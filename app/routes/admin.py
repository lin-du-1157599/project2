"""
Module: Admin Home Route

This module defines the endpoint for the admin homepage in the login application.
It includes role-based access control to ensure only admin users can access this page.
Unauthorized users are either redirected or shown a 403 error.
"""
from app.config import constants
from app import app
from flask import request, redirect, render_template, session, url_for
from app.db import db
from app.routes.user import login
# Importing decorators from the current package
from app.utils.decorators import role_required, login_required


@app.route('/admin/home')
@role_required(constants.USER_ROLE_ADMIN)
def admin_home():
     """Admin Homepage endpoint.

     Methods:
     - get: Renders the homepage for the current admin user, or an "Access
          Denied" 403: Forbidden page if the current user has a different role.

     If the user is not logged in, requests will redirect to the login page.
     """
     return render_template(constants.TEMPLATE_ADMIN_HOME)


@app.route('/all_users')
def all_users():
     return users(all_users=True)


@app.route('/system_users')
def system_users():
     return users()


@login_required
@role_required(constants.USER_ROLE_ADMIN)
def users(all_users=False):
     sqlStr = "SELECT user_id, username, email, first_name, last_name, role, status FROM users WHERE role IN ('editor', 'admin') ORDER BY username, last_name, first_name;"

     if all_users:
          sqlStr = "SELECT user_id, username, email, first_name, last_name, role, status FROM users ORDER BY username, last_name, first_name;"

     with db.get_cursor() as cursor:
          cursor.execute(sqlStr)
          userslist = cursor.fetchall()
          return render_template(constants.TEMPLATE_USER, userslist=userslist, all_users=all_users)

@app.route('/users/search_all_users', methods=[constants.HTTP_METHOD_GET])
@role_required(constants.USER_ROLE_ADMIN)
def search_all_users():
    return search_users(all_users=True)

@app.route('/users/search_system_users', methods=[constants.HTTP_METHOD_GET])
@role_required(constants.USER_ROLE_ADMIN)
def search_system_users():
    return search_users()

def search_users(all_users=False):
    searchterm = request.args.get(constants.SEARCH_TERM)
    sqlsearch = f'%{searchterm}%'
    searchcat = request.args.get(constants.SEARCH_CATEGORY)

    role_condition = "" if all_users else "AND role IN ('editor', 'admin')"

    with db.get_cursor() as cursor:
        if searchcat == constants.USERNAME:
            cursor.execute(
                f"SELECT username, first_name, last_name, email, role, status, user_id FROM users WHERE username LIKE %s {role_condition} ORDER BY username, last_name, first_name;",
                (sqlsearch,))
        elif searchcat == constants.LAST_NAME:
            cursor.execute(
                f"SELECT username, first_name, last_name, email, role, status, user_id FROM users WHERE last_name LIKE %s {role_condition} ORDER BY username, last_name, first_name;",
                (sqlsearch,))
        elif searchcat == constants.FIRST_NAME:
            cursor.execute(
                f"SELECT username, first_name, last_name, email, role, status, user_id FROM users WHERE first_name LIKE %s {role_condition} ORDER BY username, last_name, first_name;",
                (sqlsearch,))
        elif searchcat == constants.USER_FULL_NAME:
            cursor.execute(
                f"SELECT username, first_name, last_name, email, role, status, user_id FROM users WHERE CONCAT(first_name, ' ', last_name) LIKE %s {role_condition} ORDER BY username, last_name, first_name;",
                (sqlsearch,))
        elif searchcat == constants.EMAIL:
            cursor.execute(
                f"SELECT username, first_name, last_name, email, role, status, user_id FROM users WHERE email LIKE %s {role_condition} ORDER BY username, last_name, first_name;",
                (sqlsearch,))

        userslist = cursor.fetchall()
        return render_template(constants.TEMPLATE_USER, userslist=userslist, all_users=all_users, keyword=searchterm, searchType=searchcat)


@app.route('/users/edit', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
@role_required(constants.USER_ROLE_ADMIN)
def edit_user():
     if request.method == constants.HTTP_METHOD_GET:
          user_id = request.args.get(constants.USER_ID)

          with db.get_cursor() as cursor:
               cursor.execute(
                    "SELECT username, email, first_name, last_name, role, status, location, personal_description, profile_image FROM users WHERE user_id = %s;",
                    (user_id,))
               user = cursor.fetchone()

          # Ensure None values are replaced with empty strings
          user = {key: (value if value is not None else '') for key, value in user.items()}

          return render_template(constants.TEMPLATE_USER_EDIT, user=user, user_id=user_id)
     elif request.method == constants.HTTP_METHOD_POST:
          user_id = request.form.get(constants.USER_ID)
          role = request.form.get(constants.USER_ROLE)
          status = request.form.get(constants.USER_STATUS)

          with db.get_cursor() as cursor:
               cursor.execute("UPDATE users SET role=%s, status=%s WHERE user_id=%s;", (role, status, user_id,))

          with db.get_cursor() as cursor:
               cursor.execute(
                    "SELECT username, email, first_name, last_name, role, status FROM users WHERE user_id = %s;",
                    (user_id,))
               user = cursor.fetchone()

          return render_template(constants.TEMPLATE_USER_EDIT, user=user, user_id=user_id)


@app.route('/users/update', methods=[constants.HTTP_METHOD_GET, constants.HTTP_METHOD_POST])
@login_required
@role_required(constants.USER_ROLE_ADMIN)
def update_user_status():
     user_id = request.form.get(constants.USER_ID)
     user_new_role = request.form.get(constants.USER_ROLE)
     user_new_status = request.form.get(constants.USER_STATUS)

     with db.get_cursor() as cursor:
          cursor.execute("UPDATE users SET role=%s, status=%s WHERE user_id=%s;",
                         (user_new_role, user_new_status, user_id,))
     return redirect(url_for('edit_user', user_id=user_id))