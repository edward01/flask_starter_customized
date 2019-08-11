# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

bp = Blueprint("public", __name__)

@bp.route("/")
def landing():
    return render_template('public/landing.html')


@bp.route("/about")
def about():
    return render_template("public/about.html")
