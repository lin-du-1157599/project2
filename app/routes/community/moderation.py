"""
Module: Moderation Routes

This module defines the endpoints for moderating reported comments.
"""
from app import app
from flask import render_template, redirect, request, session, url_for, flash, jsonify
from app.config import constants
from app.utils.decorators import login_required, login_and_role_required
from app.db import db
from datetime import datetime


@app.route('/moderation/reported-comments')
@login_and_role_required([constants.USER_ROLE_MODERATOR, constants.USER_ROLE_EDITOR, constants.USER_ROLE_ADMIN])
def reported_comments():
    """View all reported comments."""
    with db.get_cursor() as cursor:
        cursor.execute("""
                       SELECT r.report_id,
                              r.comment_id,
                              r.reported_by,
                              r.reason,
                              r.report_time,
                              r.reviewed_by,
                              r.review_action,
                              r.reviewed_at,
                              c.content,
                              c.event_id,
                              c.user_id    as comment_author_id,
                              c.created_at as comment_created_at,
                              u1.username  as reporter_username,
                              u2.username  as author_username,
                              u3.username  as reviewer_username,
                              e.title      as event_title
                       FROM comment_reports r
                                JOIN event_comments c ON r.comment_id = c.comment_id
                                JOIN users u1 ON r.reported_by = u1.user_id
                                JOIN users u2 ON c.user_id = u2.user_id
                                LEFT JOIN users u3 ON r.reviewed_by = u3.user_id
                                JOIN events e ON c.event_id = e.event_id
                       WHERE r.review_action IS NULL
                       ORDER BY r.report_time DESC
                       """)
        pending_reports = cursor.fetchall()

        cursor.execute("""
                       SELECT r.report_id,
                              r.comment_id,
                              r.reported_by,
                              r.reason,
                              r.report_time,
                              r.reviewed_by,
                              r.review_action,
                              r.reviewed_at,
                              c.content,
                              c.event_id,
                              c.user_id    as comment_author_id,
                              c.created_at as comment_created_at,
                              u1.username  as reporter_username,
                              u2.username  as author_username,
                              u3.username  as reviewer_username,
                              e.title      as event_title
                       FROM comment_reports r
                                JOIN event_comments c ON r.comment_id = c.comment_id
                                JOIN users u1 ON r.reported_by = u1.user_id
                                JOIN users u2 ON c.user_id = u2.user_id
                                LEFT JOIN users u3 ON r.reviewed_by = u3.user_id
                                JOIN events e ON c.event_id = e.event_id
                       WHERE r.review_action IS NOT NULL
                       ORDER BY r.reviewed_at DESC
                       LIMIT 50
                       """)
        reviewed_reports = cursor.fetchall()

    return render_template('moderation/reported_comments.html',
                           pending_reports=pending_reports,
                           reviewed_reports=reviewed_reports)


@app.route('/api/moderation/review-comment', methods=[constants.HTTP_METHOD_POST])
@login_and_role_required([constants.USER_ROLE_MODERATOR, constants.USER_ROLE_EDITOR, constants.USER_ROLE_ADMIN])
def review_comment():
    """Review a reported comment.

    JSON payload should include:
    - report_id: ID of the report
    - action: 'keep', 'hidden', or 'escalated'
    """
    data = request.json
    report_id = data.get('report_id')
    action = data.get('action')
    user_id = session[constants.USER_ID]

    # Validate inputs
    if not all([report_id, action]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    if action not in ['keep', 'hidden', 'escalated']:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400

    # Check if report exists and is not already reviewed
    with db.get_cursor() as cursor:
        cursor.execute("""
                       SELECT r.*, c.comment_id
                       FROM comment_reports r
                                JOIN event_comments c ON r.comment_id = c.comment_id
                       WHERE r.report_id = %s
                       """, (report_id,))
        report = cursor.fetchone()

        if not report:
            return jsonify({'success': False, 'message': 'Report not found'}), 404

        if report['review_action']:
            return jsonify({'success': False, 'message': 'Report already reviewed'}), 400

    # Update the report with the review action
    with db.get_cursor() as cursor:
        cursor.execute("""
                       UPDATE comment_reports
                       SET review_action = %s,
                           reviewed_by   = %s,
                           reviewed_at   = %s
                       WHERE report_id = %s
                       """, (action, user_id, datetime.now(), report_id))

        # If action is 'hidden', hide the comment
        if action == 'hidden':
            cursor.execute("""
                           UPDATE event_comments
                           SET is_hidden = 1
                           WHERE comment_id = %s
                           """, (report['comment_id'],))

    return jsonify({
        'success': True,
        'message': 'Comment reviewed successfully'
    })