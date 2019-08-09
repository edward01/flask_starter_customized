# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
# from flask_caching import Cache
# from flask_webpack import Webpack

debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
# cache = Cache()
# webpack = Webpack()
