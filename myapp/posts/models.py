# -*- coding: utf-8 -*-
"""Post models."""
import datetime as dt

from ..database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)


class Post(SurrogatePK, Model):
    __tablename__ = "posts"
    title = Column(db.String(100))
    body = Column(db.Text())
    timestamp = Column(db.DateTime, index=True, default=dt.datetime.utcnow)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="posts")

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Post({body})>".format(body=self.body)

    def __init__(self, title, body, **kwargs):
        """Create instance."""
        db.Model.__init__(self, title=title, body=body, **kwargs)
