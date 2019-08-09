# -*- coding: utf-8 -*-
"""Posts section"""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from flask_login import current_user, login_required

from ..extensions import login_manager
from ..utils import flash_errors
from ..users.models import User
from .forms import PostForm
from .models import Post

blueprint = Blueprint("posts", __name__, url_prefix="/posts", static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def index():
    current_app.logger.info("---> %s|%s" % (request.endpoint, request.method))
    form = PostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.get_by_id(current_user.get_id())
            Post.create(
                title=form.title.data,
                body=form.body.data,
                user=user,
            )
            flash("Blog created", "success")
            return redirect(url_for(".index"))
        else:
            flash_errors(form)
            return redirect(url_for(".add"))
    posts = Post.query.all()
    return render_template("posts/index.html", posts=posts)


@blueprint.route("/add")
@login_required
def add():
    current_app.logger.info("---> %s|%s" % (request.endpoint, request.method))
    form = PostForm()
    return render_template("posts/add.html", form=form)


@blueprint.route("/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit(post_id):
    current_app.logger.info("---> %s|%s" % (request.endpoint, request.method))
    form = PostForm(record_id=post_id)
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        if form.validate_on_submit():
            post.update(
                title=form.title.data,
                body=form.body.data,
            )
            flash("Blog updated", "success")
            return redirect(url_for(".edit", post_id=post.id))
        else:
            flash_errors(form)
    return render_template("posts/edit.html", form=form, post=post)


@blueprint.route("/<int:post_id>/view")
def view(post_id):
    current_app.logger.info("---> %s|%s" % (request.endpoint, request.method))
    post = Post.query.get_or_404(post_id)
    return render_template("posts/view.html", post=post)


@blueprint.route("/<int:post_id>/delete")
def delete(post_id):
    current_app.logger.info("---> %s|%s" % (request.endpoint, request.method))
    post = Post.query.get_or_404(post_id)
    post.delete()
    flash("Blog deleted", "success")
    return redirect(url_for(".index"))
