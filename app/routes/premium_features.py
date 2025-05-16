from app import app
from flask import redirect, render_template, request, session, url_for, flash
from app.config import constants
from app.utils.decorators import login_required, login_and_role_required
from datetime import date
from dateutil.relativedelta import relativedelta 

from app.db import db

@app.route('/subscription')
@login_required
def subscription():
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT * FROM subscriptions WHERE is_admin_grantable = %s 
        """, (constants.USER_IS_ADMIN_GRANTABLE_NO,))
        subscriptions = cursor.fetchall()
    return render_template(constants.TEMPLATE_SUBSCRIPTION, subscriptions=subscriptions)

@app.route('/start_trial')
@login_and_role_required([constants.USER_ROLE_TRAVELLER])
def start_trial():
    if session.get(constants.USER_IS_TRIAL_USED) == 1:
        flash("You have already used the free trial.", constants.FLASH_MESSAGE_DANGER)
        return redirect(url_for(constants.URL_SUBSCRIPTION))
    
    user_id = session.get(constants.USER_ID)

    try:
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT subscription_id FROM subscriptions WHERE name = %s 
            """, (constants.SUBSCRIPTIONS_NAME_FREE_TRIAL,))
            subscription = cursor.fetchone()

        if not subscription:
            flash("No free trial available.", constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for(constants.URL_SUBSCRIPTION))

        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE users SET subscription_status = %s, is_trial_used = %s 
                WHERE user_id = %s
            """, (constants.USER_SUBSCRIPTION_TRIAL, constants.USER_IS_TRIAL_USED_YES, user_id))

            start_date = date.today()
            end_date = start_date + relativedelta(months=+1)
            cursor.execute("""
                INSERT INTO user_subscriptions (user_id, subscription_id, remaining_months, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, subscription[constants.SUBSCRIPTION_ID], 1, start_date, end_date))

        session[constants.USER_IS_TRIAL_USED] = constants.USER_IS_TRIAL_USED_YES
        flash("Your 1-month free trial has started!", constants.FLASH_MESSAGE_SUCCESS)

    except Exception as e:
        flash("An error occurred. Please try again later.", constants.FLASH_MESSAGE_DANGER)
        print("Error:", e)

    return redirect(url_for(constants.URL_SUBSCRIPTION))
