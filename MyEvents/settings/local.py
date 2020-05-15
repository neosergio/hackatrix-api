"""
Set this environment variable
DJANGO_SETTINGS_MODULE=MyEvents.settings.local
"""

from .base import *  # noqa: F403


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o^1*t5#saem!j3#ipc$zgmmwsg*#3n1ee$$h*zorr^j7@7ef!b'  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

ALLOWED_HOSTS = ['127.0.0.1']


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # noqa: F405
    }
}
