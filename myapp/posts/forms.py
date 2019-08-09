# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import Post


class PostForm(FlaskForm):
    """Register form."""

    title = StringField(
        "Title", validators=[DataRequired(), Length(min=10, max=100)]
    )
    body = StringField(
        "Body", validators=[DataRequired(), Length(min=10)]
    )

    def validate(self):
        """Validate the form."""
        initial_validation = super(PostForm, self).validate()
        if not initial_validation:
            return False
        post = Post.query.filter_by(title=self.title.data).first()
        if post:
            self.title.errors.append("Title already exists")
            return False
        return True
