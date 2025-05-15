from app import app
from flask import redirect, render_template, request, session, url_for, flash
from app.config import constants
from app.utils.decorators import login_required

from app.db import db

@app.route('/subscription')
@login_required
def subscription():
    return render_template(constants.TEMPLATE_SUBSCRIPTION)