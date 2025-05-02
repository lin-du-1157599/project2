from app.db import db

def user_profile_sidebar(user_id):
    with db.get_cursor() as cursor:
        cursor.execute('SELECT username, location, personal_description, profile_image FROM users WHERE user_id = %s;', (user_id,))
        userDetails = cursor.fetchone()
        return userDetails
