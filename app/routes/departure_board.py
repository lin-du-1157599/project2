from flask import render_template
from app import app
from app.config import constants
from app.db import db
from app.utils.decorators import login_required, subscription_required

@app.route('/departure_board', methods=[constants.HTTP_METHOD_GET])
@subscription_required
@login_required
def departure_board():
    return render_template(constants.TEMPLATE_DEPARTURE_BOARD)