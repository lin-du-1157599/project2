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
    
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT subscription_id FROM subscriptions WHERE name = %s 
        """, (constants.SUBSCRIPTIONS_NAME_FREE_TRIAL,))
        subscription = cursor.fetchone()

        if not subscription:
            flash("No free trial available.", constants.FLASH_MESSAGE_DANGER)
            return redirect(url_for(constants.URL_SUBSCRIPTION))
    process_subscription(constants.USER_SUBSCRIPTION_TRIAL, constants.USER_IS_TRIAL_USED_YES, subscription[constants.SUBSCRIPTION_ID], constants.SUBSCRIPTIONS_DURATION_MONTHS_ONE, 
                         None, None, None, None, None)
    return redirect(url_for(constants.URL_SUBSCRIPTION))

def process_subscription(subscription_status, is_trial_used, subscription_id, duration_months, 
                         billing_country, card_number, expiry_date, cvv, amount_paid):
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)
        params = [subscription_status]
        sql = "UPDATE users SET subscription_status = %s"
        if is_trial_used is not None:
            sql += ", is_trial_used = %s"
            params.append(is_trial_used)
        sql += " WHERE user_id = %s"
        params.append(session.get(constants.USER_ID))
        cursor.execute(sql, tuple(params))

        start_date = date.today()
        end_date = start_date + relativedelta(months=+duration_months)
        cursor.execute("""
            INSERT INTO user_subscriptions (user_id, subscription_id, remaining_months, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (session.get(constants.USER_ID), subscription_id, duration_months, start_date, end_date))

        if is_trial_used is not None:
            session[constants.USER_IS_TRIAL_USED] = constants.USER_IS_TRIAL_USED_YES
        else:
            subscription_payment(billing_country, card_number, expiry_date, cvv, amount_paid, cursor)

        flash(f"Your {duration_months}-month{'s' if duration_months != 1 else ''} free trial has started!", constants.FLASH_MESSAGE_SUCCESS)
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        flash("An error occurred. Please try again later.", constants.FLASH_MESSAGE_DANGER)
        print("Error:", e)
    finally:
        if cursor:
            cursor.close()

def subscription_payment(billing_country, card_number, expiry_date, cvv, amount_paid, cursor):
    print('')
    # cursor.execute("""
    #         INSERT INTO subscription_payments (user_id, billing_country, amount_paid, gst_amount, currency, card_number, expiry_date, cvv, user_subscription_id)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    #     """, (session.get(constants.USER_ID), subscription_id, duration_months, start_date, end_date))

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
    subscription_id = request.form.get(constants.SUBSCRIPTION_ID)
    card_number = request.form.get(constants.PAYMENT_CARD_NUMBER)
    expiry_date = request.form.get(constants.PAYMENT_EXPIRY_DATE)
    cvv = request.form.get(constants.PAYMENT_CVV)
    billing_country = request.form.get(constants.PAYMENT_BILLING_COUNTRY)
    duration_months_str = request.form.get(constants.SUBSCRIPTION_DURATION_MONTHS)
    duration_months = int(duration_months_str) if duration_months_str else None

    if not (card_number and expiry_date and cvv and billing_country):
        subscription = {
            constants.SUBSCRIPTION_ID: subscription_id,
            constants.PAYMENT_CARD_NUMBER: card_number,
            constants.PAYMENT_EXPIRY_DATE: expiry_date,
            constants.PAYMENT_CVV: cvv,
            constants.PAYMENT_BILLING_COUNTRY: billing_country,
            constants.SUBSCRIPTION_DURATION_MONTHS: duration_months
        }
        flash("Please fill in all payment details.",constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_PAYMENT, subscription=subscription)
    
    process_subscription(constants.USER_SUBSCRIPTION_PREMIUM, None, subscription_id, duration_months, billing_country, card_number, expiry_date, cvv, amount_paid)

    if True:
        flash(f"Payment successful! Thank you for subscribing.", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Payment failed. Please try again.", "danger")
        return redirect(url_for('payment_page', subscription_id=subscription_id))
