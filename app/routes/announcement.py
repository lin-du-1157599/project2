"""
Module: Announcement Routes

This module defines the endpoints for announcement management in the travel journal application.
It includes functionality for adding and viewing announcements
"""

from app import app
from app.config import constants
from app.db import db
from app.utils.decorators import login_required, role_required
from flask import request, redirect, render_template, session, url_for, flash

from app.utils.validators import validate_announcement


@app.route('/announcements', methods=[constants.HTTP_METHOD_GET])
@login_required
def announcements_list():
    user_role = session[constants.USER_ROLE]

    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM announcements ORDER BY created_time DESC")
        announcementsList = cursor.fetchall()
        return render_template(constants.TEMPLATE_ANNOUNCEMENTS, announcementsList = announcementsList, user_role = user_role)

@app.route('/announcements/view/<int:announcement_id>', methods=[constants.HTTP_METHOD_GET])
@login_required
def announcements_detail(announcement_id):
    with db.get_cursor() as cursor:
        cursor.execute("""
                       SELECT * FROM announcements
                       WHERE announcement_id = %s
                       """, (announcement_id,))
        announcement = cursor.fetchone()

        return render_template(constants.TEMPLATE_VIEW_ANNOUNCEMENTS, announcement = announcement)

@app.route('/announcements/add', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@role_required(constants.USER_ROLE_ADMIN)
def add_announcement():
    user_id = session[constants.USER_ID]
    if request.method == constants.HTTP_METHOD_GET:
        return render_template(constants.TEMPLATE_ADD_ANNOUNCEMENT)
    print (request.form)
    
    title = request.form[constants.TITLE]
    content = request.form[constants.CONTENT]

    # Validate announcement form fields
    is_valid, errors = validate_announcement(title, content)
    
    if not is_valid:
        for error in errors:
            flash(error, constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_ADD_ANNOUNCEMENT, title = title, content = content)

    with db.get_cursor() as cursor:
        cursor.execute("""
                       INSERT INTO announcements (user_id, title, content)
                       VALUES(%s, %s, %s)
                       """,
                       (user_id, title, content)
                    )
    flash ('Announcement created successfully!', constants.FLASH_MESSAGE_SUCCESS)
    return redirect(url_for(constants.URL_ANNOUNCEMENTS))
