# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import os
from environs import Env

APP_TITLE = 'My App'
APP_NAME = 'myapp'

env = Env()
env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SECRET_KEY = env.str("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
WEBPACK_MANIFEST_PATH = "webpack/manifest.json"
LOG_TO_STDOUT = env.bool("LOG_TO_STDOUT", default=True)
