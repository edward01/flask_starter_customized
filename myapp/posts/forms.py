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

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(PostForm, self).__init__(*args, **kwargs)
        self.record_id = kwargs.get('record_id')

    def validate(self):
        """Validate the form."""
        initial_validation = super(PostForm, self).validate()
        if not initial_validation:
            return False

        # Unique validation
        filters = [Post.title == self.title.data]
        if self.record_id is not None:  # edit mode
            filters.append(Post.id != self.record_id)
        if Post.query.filter(*tuple(filters)).first():
            self.title.errors.append("Title already exists")
            return False
        return True
