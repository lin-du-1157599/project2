"""
Module: Event Management Routes

This module defines the endpoints for event management in the travel journal application.
It includes functionality for adding, editing, deleting, and viewing events.
"""
from app import app
from flask import redirect, render_template, request, session, url_for, flash
from app.config import constants
from app.utils.decorators import login_required, role_required, login_and_role_required
from app.db import db
from app.utils.helpers import allowed_file
from app.utils.achievement import AchievementUtils
from werkzeug.utils import secure_filename
import os
from datetime import datetime

@app.route('/journey/<int:journey_id>/events')
@login_required
def view_events(journey_id):
    """View all events for a specific journey.
    
    Args:
        journey_id (int): The ID of the journey to view events for.
    """
    with db.get_cursor() as cursor:
        # Get journey details
        cursor.execute("""
            SELECT j.*, u.username 
            FROM journeys j 
            JOIN users u ON j.user_id = u.user_id 
            WHERE j.journey_id = %s
        """, (journey_id,))
        journey = cursor.fetchone()
        
        if not journey:
            flash('Journey not found', 'error')
            return redirect(url_for('traveller_home'))
            
        # Get all events for this journey
        cursor.execute("""
            SELECT * FROM events 
            WHERE journey_id = %s 
            ORDER BY start_time ASC
        """, (journey_id,))
        events = cursor.fetchall()
        
    return render_template('event/events.html', journey=journey, events=events)


@app.route('/journey/<int:journey_id>/event/add', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
def add_event(journey_id):
    """Add a new event to a journey.

    Args:
        journey_id (int): The ID of the journey to add the event to.
    """
    user_id = session[constants.USER_ID]

    # Get journey and location data needed for both GET and POST methods
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT j.*, u.username 
            FROM journeys j 
            JOIN users u ON j.user_id = u.user_id 
            WHERE j.journey_id = %s
        """, (journey_id,))
        journey = cursor.fetchone()

        if not journey:
            flash('Journey not found', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for('traveller_home'))

        # Get all locations for datalist
        cursor.execute("""
            SELECT DISTINCT location FROM events
            WHERE location IS NOT NULL AND location != ''
            ORDER BY location
        """)
        all_locations = [row['location'] for row in cursor.fetchall()]

    if request.method == constants.HTTP_METHOD_GET:
        return render_template('event/add_event.html', journey=journey, user_id=user_id, all_locations=all_locations)

    elif request.method == constants.HTTP_METHOD_POST:
        # Create a form_data dictionary to store submitted values
        form_data = {
            'title': request.form.get('title', ''),
            'description': request.form.get('description', ''),
            'start_time': request.form.get('start_time', ''),
            'end_time': request.form.get('end_time', ''),
            'location': request.form.get('location', '')
        }

        # Validate required fields
        if not form_data['title'] or not form_data['start_time'] or not form_data['location']:
            flash('Title, start time, and location are required', constants.FLASH_MESSAGE_DANGER)
            # Re-render the form with submitted data instead of redirecting
            return render_template('event/add_event.html',
                                  journey=journey,
                                  user_id=user_id,
                                  all_locations=all_locations,
                                  form_data=form_data)

        # Get journey start date for validation
        with db.get_cursor() as cursor:
            cursor.execute("""
                    SELECT start_date FROM journeys
                    WHERE journey_id = %s
                """, (journey_id,))
            journey_data = cursor.fetchone()

        if not journey_data:
            flash('Journey not found', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for('traveller_home'))

        # Convert string inputs to datetime objects for comparison
        event_start_dt = datetime.strptime(form_data['start_time'], '%Y-%m-%dT%H:%M')
        journey_start_dt = journey_data['start_date']

        # Validate event start time against journey start date
        if event_start_dt < journey_start_dt:
            flash('Event start time cannot be earlier than journey start date', constants.FLASH_MESSAGE_DANGER)
            # Re-render the form with submitted data instead of redirecting
            return render_template('event/add_event.html',
                                  journey=journey,
                                  user_id=user_id,
                                  all_locations=all_locations,
                                  form_data=form_data)

        # Validate end time if provided
        if form_data['end_time'] and form_data['end_time'].strip():
            start_dt = event_start_dt
            end_dt = datetime.strptime(form_data['end_time'], '%Y-%m-%dT%H:%M')
            if end_dt <= start_dt:
                flash('End time must be after start time', constants.FLASH_MESSAGE_DANGER)
                # Re-render the form with submitted data instead of redirecting
                return render_template('event/add_event.html',
                                      journey=journey,
                                      user_id=user_id,
                                      all_locations=all_locations,
                                      form_data=form_data)
        else:
            form_data['end_time'] = None

        # Handle image upload if provided
        event_image = None
        if 'event_image' in request.files:
            file = request.files['event_image']
            if file and file.filename:  # Check if a file was actually selected
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config[constants.IMAGE_UPLOAD_FOLDER], filename))
                    event_image = filename
                else:
                    flash('Invalid file type. Please upload a JPG, PNG, or GIF.', constants.FLASH_MESSAGE_DANGER)
                    # Re-render the form with submitted data instead of redirecting
                    return render_template('event/add_event.html',
                                          journey=journey,
                                          user_id=user_id,
                                          all_locations=all_locations,
                                          form_data=form_data)

        # Insert event into database
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO events (journey_id, title, description, start_time, end_time, location, event_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (journey_id, form_data['title'], form_data['description'],
                  form_data['start_time'], form_data['end_time'], form_data['location'], event_image))
            
            # Check for Event Creator achievement
            AchievementUtils.check_event_creator_achievement(user_id)
            # Check for Location Explorer achievement (5 unique locations)
            AchievementUtils.check_location_explorer_achievement(user_id)
            # Check for Long Voyager achievement (journey > 30 days)
            AchievementUtils.check_long_voyager_achievement(user_id, journey_id)

        # Update the `update_date` of a journey
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE journeys SET update_date = CURRENT_TIMESTAMP WHERE journey_id = %s
                           """, (journey_id,))

        flash('Event added successfully', constants.FLASH_MESSAGE_SUCCESS)
        return redirect(url_for('view_journey', journey_id=journey_id, mode=constants.MODE_ALL))


@app.route('/event/<int:event_id>/edit', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
def edit_event(event_id):
    """Edit an existing event.

    Args:
        event_id (int): The ID of the event to edit.
    """

    if request.method == constants.HTTP_METHOD_GET:
        journey_id = request.args.get(constants.JOURNEY_ID)
        mode = request.args.get(constants.REQUEST_MODE)

        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT e.*, j.journey_id, j.title as journey_title, u.username
                FROM events e
                JOIN journeys j ON e.journey_id = j.journey_id
                JOIN users u ON j.user_id = u.user_id
                WHERE e.event_id = %s
            """, (event_id,))
            event = cursor.fetchone()

            if not event:
                flash('Event not found', constants.FLASH_MESSAGE_DANGER)
                return redirect(url_for('traveller_home'))

            # Get all locations for datalist
            cursor.execute("""
                SELECT DISTINCT location FROM events
                WHERE location IS NOT NULL AND location != ''
                ORDER BY location
            """)
            all_locations = [row['location'] for row in cursor.fetchall()]

        return render_template('event/edit_event.html',
                               event=event,
                               journey_id=journey_id,
                               mode=mode,
                               all_locations=all_locations)

    elif request.method == constants.HTTP_METHOD_POST:
        # Create a dictionary to store the form data
        form_data = {
            'title': request.form.get('title', ''),
            'description': request.form.get('description', ''),
            'start_time': request.form.get('start_time', ''),
            'end_time': request.form.get('end_time', ''),
            'location': request.form.get('location', ''),
            'journey_id': request.form.get(constants.JOURNEY_ID),
            'mode': request.form.get('mode', constants.MODE_ALL),
            'remove_image': request.form.get('remove_image') == 'on'
        }

        # Get existing event data for recreating the event object
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT e.*, j.journey_id, j.title as journey_title, u.username
                FROM events e
                JOIN journeys j ON e.journey_id = j.journey_id
                JOIN users u ON j.user_id = u.user_id
                WHERE e.event_id = %s
            """, (event_id,))
            db_event = cursor.fetchone()

            if not db_event:
                flash('Event not found', constants.FLASH_MESSAGE_DANGER)
                return redirect(url_for('traveller_home'))

            # Get all locations for datalist
            cursor.execute("""
                SELECT DISTINCT location FROM events
                WHERE location IS NOT NULL AND location != ''
                ORDER BY location
            """)
            all_locations = [row['location'] for row in cursor.fetchall()]

        # Create a modified event object with form data for template rendering
        event = dict(db_event)
        event['title'] = form_data['title']
        event['description'] = form_data['description']

        # Handle datetime fields for display if validation fails
        try:
            event['start_time'] = datetime.strptime(form_data['start_time'], '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError):
            event['start_time'] = db_event['start_time']

        if form_data['end_time'] and form_data['end_time'].strip():
            try:
                event['end_time'] = datetime.strptime(form_data['end_time'], '%Y-%m-%dT%H:%M')
            except (ValueError, TypeError):
                event['end_time'] = db_event['end_time']
        else:
            event['end_time'] = None

        event['location'] = form_data['location']

        # Validate required fields
        if not form_data['title'] or not form_data['start_time'] or not form_data['location']:
            flash('Title, start time, and location are required', constants.FLASH_MESSAGE_DANGER)
            return render_template('event/edit_event.html',
                                   event=event,
                                   journey_id=form_data['journey_id'],
                                   mode=form_data['mode'],
                                   all_locations=all_locations)

        # Get journey start date for validation
        with db.get_cursor() as cursor:
            cursor.execute("""
                        SELECT start_date FROM journeys
                        WHERE journey_id = %s
                    """, (form_data['journey_id'],))
            journey_data = cursor.fetchone()

        if not journey_data:
            flash('Journey not found', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for('traveller_home'))

        # Convert string inputs to datetime objects for comparison
        try:
            event_start_dt = datetime.strptime(form_data['start_time'], '%Y-%m-%dT%H:%M')
            journey_start_dt = journey_data['start_date']

            # Validate event start time against journey start date
            if event_start_dt < journey_start_dt:
                flash('Event start time cannot be earlier than journey start date', constants.FLASH_MESSAGE_DANGER)
                return render_template('event/edit_event.html',
                                       event=event,
                                       journey_id=form_data['journey_id'],
                                       mode=form_data['mode'],
                                       all_locations=all_locations)

            # Validate end time if provided
            if form_data['end_time'] and form_data['end_time'].strip():
                end_dt = datetime.strptime(form_data['end_time'], '%Y-%m-%dT%H:%M')
                if end_dt <= event_start_dt:
                    flash('End time must be after start time', constants.FLASH_MESSAGE_DANGER)
                    return render_template('event/edit_event.html',
                                           event=event,
                                           journey_id=form_data['journey_id'],
                                           mode=form_data['mode'],
                                           all_locations=all_locations)
            else:
                form_data['end_time'] = None
        except ValueError:
            # Handle datetime parsing errors
            flash('Invalid date format', constants.FLASH_MESSAGE_DANGER)
            return render_template('event/edit_event.html',
                                   event=event,
                                   journey_id=form_data['journey_id'],
                                   mode=form_data['mode'],
                                   all_locations=all_locations)

        # Get current event image
        with db.get_cursor() as cursor:
            cursor.execute("SELECT event_image FROM events WHERE event_id = %s", (event_id,))
            current_image = cursor.fetchone()['event_image']

        # Handle image upload if provided
        event_image = None
        if 'event_image' in request.files:
            file = request.files['event_image']
            if file and file.filename:  # Check if a file was actually selected
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config[constants.IMAGE_UPLOAD_FOLDER], filename))
                    event_image = filename

                    # Delete old image if replacing
                    if current_image:
                        try:
                            os.remove(os.path.join(app.config[constants.IMAGE_UPLOAD_FOLDER], current_image))
                        except:
                            pass  # Ignore errors if file doesn't exist
                else:
                    flash('Invalid file type. Please upload a JPG, PNG, or GIF.', constants.FLASH_MESSAGE_DANGER)
                    return render_template('event/edit_event.html',
                                           event=event,
                                           journey_id=form_data['journey_id'],
                                           mode=form_data['mode'],
                                           all_locations=all_locations)

        # Handle image removal
        if form_data['remove_image'] and current_image:
            try:
                os.remove(os.path.join(app.config[constants.IMAGE_UPLOAD_FOLDER], current_image))
            except:
                pass  # Ignore errors if file doesn't exist

        image_value = event['event_image']
        if event_image:
            image_value = event_image
        elif form_data['remove_image']:
            image_value = None

        # Update event in database
        with db.get_cursor() as cursor:
            cursor.execute("""
                       UPDATE events 
                       SET title = %s, description = %s, start_time = %s, end_time = %s, 
                           location = %s, event_image = %s
                       WHERE event_id = %s
                   """, (form_data['title'], form_data['description'], form_data['start_time'], form_data['end_time'],
                         form_data['location'], image_value,
                         event_id))
        # Update the `update_date` of a journey
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE journeys SET update_date = CURRENT_TIMESTAMP WHERE journey_id = %s
                           """, (form_data['journey_id'],))
        # Check for Long Voyager achievement (journey > 30 days)
        AchievementUtils.check_long_voyager_achievement(user_id, form_data['journey_id'])
        flash('Event updated successfully', constants.FLASH_MESSAGE_SUCCESS)
        return redirect(url_for('view_journey', journey_id=form_data['journey_id'], mode=form_data['mode']))

@app.route('/journey/<int:journey_id>/event/<int:event_id>/delete', methods=[constants.HTTP_METHOD_GET])
@login_required
def delete_event(journey_id, event_id, mode='all'):
    """Delete an event from a journey.

    Args:
        journey_id (int): The ID of the journey containing the event.
        event_id (int): The ID of the event to delete.
        mode (str): The mode to return to after deletion (all or public).

    Returns:
        A redirect to the journey view page.
    """
    user_id = session[constants.USER_ID]
    mode = request.args.get(constants.REQUEST_MODE, 'all')

    # Verify the event exists and belongs to the specified journey
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT e.*, j.user_id as journey_owner_id 
            FROM events e
            JOIN journeys j ON e.journey_id = j.journey_id
            WHERE e.event_id = %s AND j.journey_id = %s
        """, (event_id, journey_id))
        event = cursor.fetchone()

        if not event:
            flash('Event not found', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for('view_journey', journey_id=journey_id, mode=mode))

        # Check permission - only journey owner or admin/editor for public journeys can delete events
        if user_id != event['journey_owner_id'] and session['role'] not in ['editor', 'admin']:
            flash('You do not have permission to delete this event.', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for('view_journey', journey_id=journey_id, mode=mode))

    # Since we're handling the confirmation in the modal, we go straight to deletion
    with db.get_cursor() as cursor:
        # Get event image before deletion
        cursor.execute("SELECT event_image FROM events WHERE event_id = %s", (event_id,))
        result = cursor.fetchone()

        if result and result['event_image']:
            event_image = result['event_image']

            # Check if this image is used by any other events
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM events 
                WHERE event_image = %s AND event_id != %s
            """, (event_image, event_id))

            image_usage = cursor.fetchone()

            # Only delete the image if it's not used by any other events
            if image_usage['count'] == 0:
                try:
                    os.remove(os.path.join(app.config[constants.IMAGE_UPLOAD_FOLDER], event_image))
                except FileNotFoundError:
                    pass  # Ignore if file doesn't exist

        # Delete event from database
        cursor.execute("DELETE FROM events WHERE event_id = %s", (event_id,))
        # Update the `update_date` of a journey
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE journeys SET update_date = CURRENT_TIMESTAMP WHERE journey_id = %s
                           """, (journey_id,))

    flash('Event deleted successfully', constants.FLASH_MESSAGE_SUCCESS)
    return redirect(url_for('view_journey', journey_id=journey_id, mode=mode))

@app.route('/event/location', methods=[constants.HTTP_METHOD_POST])
@login_and_role_required([constants.USER_ROLE_EDITOR, constants.USER_ROLE_ADMIN])
def edit_event_location():
    """
    Edit the location of an event within public-shared journey.
    """
    # Get event ID from query parameters
    event_id = request.args.get('event_id')
    if not event_id:
        flash('Event ID is required.', constants.FLASH_MESSAGE_DANGER)
        return redirect(url_for('public_journeys'))

    # Get location from form
    new_location = request.form.get('location', '')

    # Get event details and check if journey is public
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT e.*, j.status, j.journey_id 
            FROM events e
            JOIN journeys j ON e.journey_id = j.journey_id
            WHERE e.event_id = %s
        """, (event_id,))
        event = cursor.fetchone()

        if not event:
            flash('Event not found.', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for('public_journeys'))

        # Check if journey is public
        if event['status'] != 'public':
            flash('You can only edit locations in publicly shared journeys.', constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for('public_journeys'))

        # Update the location
        cursor.execute("UPDATE events SET location = %s WHERE event_id = %s", (new_location, event_id))

    flash('Location updated successfully!', constants.FLASH_MESSAGE_SUCCESS)
    return redirect(url_for('view_journey', journey_id=event['journey_id']))