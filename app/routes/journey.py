from app import app
from flask import redirect, render_template, request, session, url_for, flash
from app.config import constants
from app.utils.decorators import login_required, login_and_role_required
from app.utils.sidebar import user_profile_sidebar

from app.db import db
from app.utils.validators import validate_journey
from datetime import datetime
import re, os
from markupsafe import Markup
from rapidfuzz import fuzz

@app.route('/myjourney', methods=[constants.HTTP_METHOD_GET])
@login_required
def myjourney():
    # session[constants.USER_ID] = account[constants.USER_ID]
    user_id = session[constants.USER_ID]
    profile = user_profile_sidebar(user_id)

    with db.get_cursor() as cursor:
        cursor.execute('''
                       SELECT journey_id, title, description, status, is_hidden, start_date, update_date 
                       FROM journeys
                       WHERE user_id = %s
                       ORDER BY start_date DESC;''',
                       (user_id,))
        journeyList = cursor.fetchall()
    return render_template(constants.TEMPLATE_MYJOURNEY, journeyList = journeyList, user_id = user_id, profile = profile)


@app.route('/journey/add', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
def add_journey():
    user_id = session[constants.USER_ID]

    # Retrieve if user are allowed to public shared journeys
    with db.get_cursor() as cursor:
        cursor.execute("SELECT shareable FROM users WHERE user_id = %s;", (user_id,))
        shareableResult = cursor.fetchone()
    
    shareable = shareableResult['shareable']

    if request.method == constants.HTTP_METHOD_GET:
        return render_template(constants.TEMPLATE_ADD_JOURNEY, shareable = shareable)
    print (request.form)
    
    title = request.form[constants.TITLE]
    description = request.form[constants.DESCRIPTION]
    start_date = request.form[constants.START_DATE]
    status = request.form.get(constants.STATUS)
    if status is None:
        status = constants.JOURNEY_STATUS_PRIVATE

    # Restricted if the user are allowed to share journey
    if shareable == 0:
        status = constants.JOURNEY_STATUS_PRIVATE

    # Validate journey data
    is_valid, errors = validate_journey(title, description, start_date, status)

    if not is_valid:
        # Flash validation errors and return to form
        for error in errors:
            flash(error, constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_ADD_JOURNEY,
                               title=title,
                               description=description,
                               start_date=start_date,
                               status=status,
                               shareable=shareable)


    with db.get_cursor() as cursor:
        cursor.execute('''
                        INSERT INTO journeys (user_id, title, description, start_date, status)
                        VALUES(%s, %s, %s, %s, %s)
                        ''',
                        (user_id, title, description, start_date, status)
                        )
    flash('Journey created successfully!', constants.FLASH_MESSAGE_SUCCESS)
    return redirect(url_for(constants.URL_MYJOURNEY))
    
@app.route('/journey/edit', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
def edit_journey():
    user_id = session[constants.USER_ID]
    user_role = session.get(constants.USER_ROLE)

    if request.method == constants.HTTP_METHOD_GET:
        journey_id = request.args.get(constants.JOURNEY_ID)
        mode = request.args.get(constants.REQUEST_MODE)

        # Check if the user is the owner of the journey.
        # If not, it will be denied to access and redirect
        # to my journey page with error message. Ensure the
        # journey only visible edit page for the owner
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT j.user_id, u.shareable
                FROM journeys j
                JOIN users u ON j.user_id = u.user_id
                WHERE journey_id = %s""",
                (journey_id,))
            journey_owner = cursor.fetchone()
            shareable = journey_owner['shareable']
            print('journey_owner: ', journey_owner)

        if mode == (constants.MODE_ALL and user_id != journey_owner['user_id']) or (mode == constants.MODE_PUBLIC and session[constants.USER_ROLE]==constants.USER_ROLE_TRAVELLER):
            flash('You do not have permission to edit this journey.', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for(constants.URL_MYJOURNEY))

        # Retrieve and display journey details in the form if the user is the owner.
        with db.get_cursor() as cursor:
            cursor.execute("SELECT title, description, start_date, status, is_hidden FROM journeys WHERE journey_id=%s;", (journey_id,))
            journey = cursor.fetchone()
            print('journey: ', journey)

        return render_template(constants.TEMPLATE_EDIT_JOURNEY, journey_id = journey_id, mode = mode, journey = journey, user_role = user_role, shareable = shareable)

    elif request.method == constants.HTTP_METHOD_POST:

        # Retrieve the d
        # Get the details submitted via the form on the signup page, and store
        # the values in temporary local variables for ease of access.
        journey_id = request.form[constants.JOURNEY_ID]
        title = request.form[constants.TITLE]
        description = request.form[constants.DESCRIPTION]
        start_date = request.form[constants.START_DATE]
        status = request.form[constants.STATUS]
        is_hidden = request.form[constants.IS_HIDDEN]
        mode = request.form[constants.REQUEST_MODE]

        # Validate input data
        is_valid, errors = validate_journey(title, description, start_date, status)
        if not is_valid:
            # Flash validation errors and return to form
            for error in errors:
                flash(error, constants.FLASH_MESSAGE_DANGER)
            return render_template(constants.TEMPLATE_EDIT_JOURNEY,
                                   journey_id=journey_id,
                                   journey={'title': title, 'description': description, 'start_date': start_date,
                                            'status': status, 'is_hidden': is_hidden},
                                   user_role = user_role)

        # When a journey is marked as hidden by ediotr/aadmin,
        # its status will also be set to 'private'
        if is_hidden == '1':
            status = 'private'
        
        # Update journey with validated data
        with db.get_cursor() as cursor:
            # Include status in the update if it was provided
            if status:
                cursor.execute("""
                                      UPDATE journeys 
                                      SET title=%s, description=%s, start_date=%s, status=%s, is_hidden=%s 
                                      WHERE journey_id=%s;
                                      """,
                               (title, description, start_date, status, is_hidden, journey_id))
        
            else:
                cursor.execute("""
                                      UPDATE journeys 
                                      SET title=%s, description=%s, start_date=%s 
                                      WHERE journey_id=%s;
                                      """,
                               (title, description, start_date, journey_id))

        flash('Journey updated successfully.', constants.FLASH_MESSAGE_SUCCESS)
    
        redirect_url = url_for(constants.URL_MYJOURNEY) if mode == constants.MODE_ALL else url_for(constants.URL_PUBLIC_JOURNEY)

        return redirect(redirect_url)

@app.route('/journey/<int:journey_id>/delete', methods=[constants.HTTP_METHOD_GET])
@login_required
def delete_journey(journey_id):
    """Delete a journey and all its associated events and images.

    Args:
        journey_id (int): The ID of the journey to delete.

    Returns:
        A redirect to the user's journey list page.
    """
    user_id = session[constants.USER_ID]
    mode = request.args.get(constants.REQUEST_MODE)

    # Check if the journey exists
    with db.get_cursor() as cursor:
        cursor.execute("SELECT journey_id, title FROM journeys WHERE journey_id=%s;", (journey_id,))
        journey = cursor.fetchone()

        if not journey:
            flash('Journey not found', 'error')
            return redirect(url_for(constants.URL_MYJOURNEY))

        # Check if the user is the owner of the journey or an admin
        cursor.execute("SELECT user_id FROM journeys WHERE journey_id=%s;", (journey_id,))
        journey_owner = cursor.fetchone()

        # Only allow the owner to delete the journey
        if user_id != journey_owner['user_id'] and session['role'] != 'admin':
            flash('You do not have permission to delete this journey.', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for(constants.URL_MYJOURNEY))

    # Since we're handling the confirmation in the modal, go straight to deletion
    with db.get_cursor() as cursor:
        # Get all event images from this journey
        cursor.execute("SELECT event_id, event_image FROM events WHERE journey_id = %s", (journey_id,))
        journey_events = cursor.fetchall()

        # For each event's image, check if it's used elsewhere before deleting
        for event in journey_events:
            if event['event_image']:
                # Check if the image is used by any other events
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM events 
                    WHERE event_image = %s AND event_id != %s
                """, (event['event_image'], event['event_id']))

                result = cursor.fetchone()

                # Only delete if this is the only event using this image
                if result['count'] == 0:
                    try:
                        os.remove(os.path.join(app.config[constants.IMAGE_UPLOAD_FOLDER], event['event_image']))
                    except FileNotFoundError:
                        pass  # Ignore if file doesn't exist

        # Delete the journey (cascades to events due to foreign key constraint)
        cursor.execute("DELETE FROM journeys WHERE journey_id = %s", (journey_id,))

    flash('Journey has been deleted successfully', constants.FLASH_MESSAGE_SUCCESS)

    # Redirect based on mode
    if mode == 'public':
        return redirect(url_for('public_journeys'))
    else:
        return redirect(url_for(constants.URL_MYJOURNEY))
    
@app.route('/journeys/public', methods=[constants.HTTP_METHOD_GET])
@login_required
def public_journeys():
    # Query to get all public journeys ordered by most recently updated
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT j.journey_id, j.title, j.description, j.update_date, j.user_id, 
                   u.username, u.first_name, u.last_name
            FROM journeys j
            JOIN users u ON j.user_id = u.user_id
            WHERE j.status = 'public' AND j.is_hidden = 0
            ORDER BY j.update_date DESC
        """)
        public_journeys = cursor.fetchall()

    return render_template(constants.TEMPLATE_PUBLIC_JOURNEY, journeyList=public_journeys)


@app.route('/journey/view/<int:journey_id>', methods=[constants.HTTP_METHOD_GET])
@login_required
def view_journey(journey_id):
    user_id = session[constants.USER_ID]
    mode = request.args.get(constants.REQUEST_MODE)
    user_role = session[constants.USER_ROLE]

    # Retrieve journey details with author information
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT j.*, u.username, u.first_name, u.last_name, u.profile_image,
                   MIN(e.start_time) as journey_start
            FROM journeys j
            JOIN users u ON j.user_id = u.user_id
            LEFT JOIN events e ON j.journey_id = e.journey_id
            WHERE j.journey_id = %s
            GROUP BY j.journey_id
        """, (journey_id,))
        journey = cursor.fetchone()

        # Check if journey exists and user has permission to view it
        if not journey:
            flash('Journey not found.', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for(constants.URL_PUBLIC_JOURNEY))

        # Check if journey is private and not owned by current user
        if journey['status'] == 'private' and journey['user_id'] != user_id:
            flash('You do not have permission to view this journey.', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for(constants.URL_PUBLIC_JOURNEY))

        # Check if journey is hidden and user is not editor or admin
        if journey['is_hidden'] == 1:
            with db.get_cursor() as role_cursor:
                role_cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
                user_role = role_cursor.fetchone()['role']

            if user_role not in [constants.USER_ROLE_EDITOR, constants.USER_ROLE_ADMIN]:
                flash('This journey is not available.', constants.FLASH_MESSAGE_DANGER)
                return redirect(url_for(constants.URL_PUBLIC_JOURNEY))

        # Get all event details for this journey
        cursor.execute("""
            SELECT * FROM events 
            WHERE journey_id = %s
            ORDER BY start_time ASC
        """, (journey_id,))
        events = cursor.fetchall()

        cursor.execute("""
            SELECT DISTINCT location FROM events
            WHERE location IS NOT NULL AND location != ''
            ORDER BY location
        """)
        all_locations = [row['location'] for row in cursor.fetchall()]

    return render_template(constants.TEMPLATE_VIEW_JOURNEY,
                           journey=journey,
                           events=events,
                           all_locations=all_locations,
                           user_role=user_role,
                           mode=mode,
                           user_id=user_id)


@app.route('/journeys/search', methods=[constants.HTTP_METHOD_GET])
@login_required
def search_public_journey():
    keyword = request.args.get('keyword', '').strip()
    searchcat = request.args.get(constants.SEARCH_CATEGORY)

    if not keyword:
        flash('Please enter a keyword to search.', constants.FLASH_MESSAGE_DANGER)
        return redirect(url_for('public_journeys'))

    query = f"%{keyword}%"
    with db.get_cursor() as cursor:
        if searchcat == constants.JOURNEY_TEXT:
            cursor.execute("""
                SELECT j.journey_id, j.title, j.description, j.update_date, j.user_id,
                       u.username, u.first_name, u.last_name
                FROM journeys j
                JOIN users u ON j.user_id = u.user_id
                WHERE j.status = 'public' AND j.is_hidden = 0
                AND (LOWER(j.title) LIKE LOWER(%s) OR LOWER(j.description) LIKE LOWER(%s))
                ORDER BY j.update_date DESC
            """, (query, query))
        elif searchcat == constants.LOCATION:
            cursor.execute("""
                SELECT DISTINCT
                           j.journey_id, j.title, j.description, j.update_date, j.user_id,
                           u.username, u.first_name, u.last_name,
                           MIN(e.location) AS location
                FROM journeys j
                JOIN users u ON j.user_id = u.user_id
                JOIN events e ON j.journey_id = e.journey_id
                WHERE j.status = 'public' AND j.is_hidden = 0
                GROUP BY j.journey_id
                ORDER BY j.update_date DESC""")
        search_results = cursor.fetchall()

    if not search_results:
        flash('No journeys found matching your search criteria.', constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_PUBLIC_JOURNEY, keyword = keyword)

    # Using if statement to check the search category.
    # If the type is JOURNEY_TEXT, highlight the keywords
    # to help users recognize them more esaily in the search results.
    # Since the location details are not displayed on the journeys page,
    # only the results are shown without highlighting.
    highlighted_results = []
    if searchcat == constants.JOURNEY_TEXT:
        for journey in search_results:
            highlighted_title = re.sub(f"({re.escape(keyword)})", r'<mark>\1</mark>', journey['title'], flags=re.IGNORECASE)
            highlighted_description = re.sub(f"({re.escape(keyword)})", r'<mark>\1</mark>', journey['description'], flags=re.IGNORECASE)
            journey['title'] = Markup(highlighted_title)
            journey['description'] = Markup(highlighted_description)
            highlighted_results.append(journey)
    else:
        # Fuzzy search by event location. 
        # Compare the input keyword from the user with
        # each journey's location,both converted to lowercase.
        # If the similarity score is greater that 80%,
        # append the journey to the result list.
        for journey in search_results:
            if fuzz.partial_ratio(keyword.lower(), journey['location'].lower()) >= 80:
                highlighted_results.append(journey)

    return render_template(constants.TEMPLATE_PUBLIC_JOURNEY, journeyList = highlighted_results, keyword = keyword, searchcat = searchcat)

@app.route('/journeys/hidden', methods=[constants.HTTP_METHOD_GET])
@login_and_role_required([constants.USER_ROLE_EDITOR, constants.USER_ROLE_ADMIN])
def hidden_journeys():
    # Query to get all hidden journeys ordered by most recently updated
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT j.journey_id, j.title, j.description, j.update_date, j.user_id,
                   u.username, u.first_name, u.last_name 
            FROM journeys j
            JOIN users u ON j.user_id = u.user_id
            WHERE j.is_hidden = 1
            ORDER BY u.username, j.update_date DESC
        """)
        hiddenJourneys = cursor.fetchall()

        # Grouped hidden journeys by username to ensure editor/admin can clearly 
        # review all publicly-shared journeys that have been hidden for each user. 
        
        # Using for loop to retrieve hidden journey list from the database. 
        # For each journey, check if username exists in the groupedJourneys dict. 
        # If not, create a new list for that users. Then append the journey to 
        # the corresponding list. Each username corresponds to a list of their hidden journeys.
        groupedJourneys = {}

        for journey in hiddenJourneys:
            username = journey['username']
            if username not in groupedJourneys:
                groupedJourneys[username] = []
            groupedJourneys[username].append(journey)

        print('grouped_journeys: ',groupedJourneys)
        return render_template(constants.TEMPLATE_HIDDEN_JOURNEY, groupedJourneys = groupedJourneys)