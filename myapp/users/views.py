# -*- coding: utf-8 -*-
"""Auth section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user

from ..extensions import login_manager
from ..utils import flash_errors
from .forms import LoginForm, RegisterForm
from .models import User

blueprint = Blueprint("users", __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/")
@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    """Login page."""
    form = LoginForm()
    current_app.logger.info("---> %s|%s" % (request.endpoint, request.method))
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for(".my_profile")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("users/login.html", form=form)


@blueprint.route("/my_profile/")
@login_required
def my_profile():
    current_app.logger.info("---> %s" % (request.endpoint))
    return render_template("users/my_profile.html")


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    current_app.logger.info("---> %s" % (request.endpoint))
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.landing"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    current_app.logger.info("---> %s" % (request.endpoint))
    form = RegisterForm()
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.landing"))
    else:
        flash_errors(form)
    return render_template("users/register.html", form=form)
