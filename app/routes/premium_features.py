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
    user_id = session[constants.USER_ID]
    user_role = session[constants.USER_ROLE]
    logged_in = session[constants.SESSION_LOGGED_IN]

    # Query subscription details
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT * FROM subscriptions WHERE is_admin_grantable = %s 
        """, (constants.USER_IS_ADMIN_GRANTABLE_NO,))
        subscriptions = cursor.fetchall()
    
    # Check if user has used free trial
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT subscription_status, is_trial_used FROM USERS WHERE user_id = %s 
        """, (user_id,))
        subDetails = cursor.fetchone()
        
    return render_template(constants.TEMPLATE_SUBSCRIPTION, subscriptions=subscriptions, subDetails = subDetails, user_role = user_role, logged_in = logged_in)

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

@app.route('/payment/<int:subscription_id>')
@login_and_role_required([constants.USER_ROLE_TRAVELLER])
def payment_page(subscription_id):
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT * FROM subscriptions WHERE subscription_id = %s 
        """, (subscription_id,))
        subscription = cursor.fetchone()
    if not subscription:
        flash("Subscription plan not found.", constants.FLASH_MESSAGE_DANGER)
        return redirect(url_for(constants.URL_SUBSCRIPTION))
    return render_template(constants.TEMPLATE_PAYMENT, subscription=subscription)

@app.route('/process_payment', methods=[constants.HTTP_METHOD_POST])
@login_and_role_required([constants.USER_ROLE_TRAVELLER])
def process_payment():
    print('payment')
