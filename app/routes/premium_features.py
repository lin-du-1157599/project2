from app import app
from flask import redirect, render_template, request, session, url_for, flash
from app.config import constants
from app.utils.decorators import login_required, login_and_role_required
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP

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
    
    try:
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT subscription_id FROM subscriptions WHERE name = %s 
            """, (constants.SUBSCRIPTIONS_NAME_FREE_TRIAL,))
            subscription = cursor.fetchone()

            if not subscription:
                flash("No free trial available.", constants.FLASH_MESSAGE_DANGER)
                return redirect(url_for(constants.URL_SUBSCRIPTION))
        process_subscription(constants.USER_SUBSCRIPTION_TRIAL, constants.USER_IS_TRIAL_USED_YES, subscription[constants.SUBSCRIPTION_ID], constants.SUBSCRIPTIONS_DURATION_MONTHS_ONE, 
                         None, None, None, None, None, None)
    except Exception as e:
        flash("An error occurred. Please try again later.", constants.FLASH_MESSAGE_DANGER)
        print("Error:", e)
        return render_template(constants.TEMPLATE_PAYMENT, subscription=subscription)
    return redirect(url_for(constants.URL_SUBSCRIPTION))

def process_subscription(subscription_status, is_trial_used, subscription_id, duration_months, 
                         billing_country, billing_address, card_number, expiry_date, cvv, amount_paid, price_nzd_excl_gst):
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT  subscription_end_date, remaining_months FROM users WHERE user_id = %s
        """, (session.get(constants.USER_ID), ))
        user = cursor.fetchone()

        sql = "UPDATE users SET subscription_status = %s, subscription_end_date = %s, remaining_months = %s"
        subscription_end_date = user[constants.USER_SUBSCRIPTION_END_DATE]
        if subscription_end_date is None:
            subscription_end_date = date.today()
        new_remaining_months = user.get(constants.USER_REMAINING_MONTHS) + duration_months
        new_end_date = subscription_end_date + relativedelta(months=+duration_months)
        params = [subscription_status, new_end_date, new_remaining_months]
        
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
        user_subscription_id = cursor.lastrowid

        if is_trial_used is not None:
            session[constants.USER_IS_TRIAL_USED] = constants.USER_IS_TRIAL_USED_YES
        else:
            subscription_payment(billing_country, billing_address, card_number, expiry_date, cvv, price_nzd_excl_gst,amount_paid, user_subscription_id, cursor)

        flash(f"Your {duration_months}-month{'s' if duration_months != 1 else ''} free trial has started!", constants.FLASH_MESSAGE_SUCCESS)
        conn.commit()
        session[constants.USER_SUBSCRIPTION_END_DATE] = new_end_date.strftime('%d/%m/%Y')
    except Exception as e:
        conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def subscription_payment(billing_country, billing_address, card_number, expiry_date, cvv, price_nzd_excl_gst, amount_paid, user_subscription_id, cursor):
    if(billing_country == constants.REQUEST_BILLING_COUNTRY_NZ):
        gst_amount = (amount_paid - price_nzd_excl_gst).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        gst_amount = 0.00
    cursor.execute("""
            INSERT INTO subscription_payments (user_id, billing_country, billing_address, amount_paid, gst_amount, card_number, expiry_date, cvv, user_subscription_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (session.get(constants.USER_ID), billing_country, billing_address, amount_paid, gst_amount, card_number, expiry_date, cvv, user_subscription_id))

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
    card_number = request.form.get(constants.PAYMENT_CARD_NUMBER).replace('-', '')
    expiry_date = request.form.get(constants.PAYMENT_EXPIRY_DATE)
    cvv = request.form.get(constants.PAYMENT_CVV)
    billing_country = request.form.get(constants.PAYMENT_BILLING_COUNTRY)
    billing_address = request.form.get(constants.PAYMENT_BILLING_ADDRESS)
    price_nzd_excl_gst = Decimal(request.form.get(constants.SUBSCRIPTION_PRICE_NZD_EXCL_GST))
    price_to_pay = Decimal(request.form.get(constants.REQUEST_PRICE_TO_PAY))
    duration_months_str = request.form.get(constants.SUBSCRIPTION_DURATION_MONTHS)
    duration_months = int(duration_months_str) if duration_months_str else None
    subscription = {
            constants.SUBSCRIPTION_ID: subscription_id,
        constants.PAYMENT_CARD_NUMBER: card_number,
        constants.PAYMENT_EXPIRY_DATE: expiry_date,
        constants.PAYMENT_CVV: cvv,
        constants.PAYMENT_BILLING_COUNTRY: billing_country,
        constants.PAYMENT_BILLING_ADDRESS: billing_address,
        constants.SUBSCRIPTION_DURATION_MONTHS: duration_months,
        constants.SUBSCRIPTION_PRICE_NZD_EXCL_GST: price_nzd_excl_gst,
        constants.REQUEST_PRICE_TO_PAY: price_to_pay
    }

    if not (card_number and expiry_date and cvv and billing_country and billing_address):
        flash("Please fill in all payment details.",constants.FLASH_MESSAGE_DANGER)
        return render_template(constants.TEMPLATE_PAYMENT, subscription=subscription)
    try:
        process_subscription(constants.USER_SUBSCRIPTION_PREMIUM, None, subscription_id, duration_months, billing_country, billing_address, card_number, expiry_date, cvv, price_to_pay, price_nzd_excl_gst)
    except Exception as e:
        flash("An error occurred. Please try again later.", constants.FLASH_MESSAGE_DANGER)
        print("Error:", e)
        return render_template(constants.TEMPLATE_PAYMENT, subscription=subscription)
    return redirect(url_for(constants.URL_SUBSCRIPTION))

@app.route('/subscription_history')
@login_required
def subscription_history():
    return render_template('subscription_history.html')
