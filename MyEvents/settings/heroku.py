"""
Set this environment variable
DJANGO_SETTINGS_MODULE=MyEvents.settings.heroku
"""

import dj_database_url
import django_heroku
from .base import *  # noqa: F403,F401
from utils.environment import env


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', '')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

ALLOWED_HOSTS = ['.herokuapp.com']


# Configure Django App for Heroku
django_heroku.settings(locals())


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

db_from_env = dj_database_url.config(conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)  # noqa: F405
