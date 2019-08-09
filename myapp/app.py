# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template

from .extensions import (
    debug_toolbar,
    db,
    migrate,
    bcrypt,
    csrf_protect,
    login_manager,
#     cache,
#     webpack,
)
from . import public, users #, commands
#-- Custom blueprints
from . import (
    posts
)


def create_app(config_object="myapp.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    debug_toolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    # cache.init_app(app)
    # webpack.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(users.views.blueprint)
    #-- Custom blueprints
    app.register_blueprint(posts.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        context_vars = {"db": db, "User": users.models.User}
        #-- Custom blueprints
        context_vars['Post'] = posts.models.Post
        return context_vars

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    # app.cli.add_command(commands.test)
    # app.cli.add_command(commands.lint)
    return None


def configure_logger(app):
    """Configure loggers."""
    # handler = logging.StreamHandler(sys.stdout)
    # if not app.logger.handlers:
    #     app.logger.addHandler(handler)

    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/%s.log' % app.config['APP_NAME'],
                                        maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('============ %s is starting... ============' % app.config['APP_NAME'])
