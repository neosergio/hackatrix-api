import time

from constance import config
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import User


def generate_user_qr_code(user):
    code_base = str(int(time.time()))
    user.one_time_use_code = code_base + str(user.id)
    user.save()
    return user.one_time_use_code


def validate_user_qr_code(code, user):
    user = get_object_or_404(User, pk=code[10:])
    code_extracted = int(code[:10])
    min_value = int(time.time()) - settings.SECONDS_TO_REFRESH_IDENTITY
    if code_extracted >= min_value:
        if code == user.one_time_use_code:
            return True
        return False
    return False


def validate_user_email(email):
    if config.USER_EMAIL_DOMAIN_RESTRICTION_FLAG:
        domains = [c.strip() for c in config.USER_EMAIL_DOMAIN_RESTRICTION.split(',')]
        email_domain = email.split('@')[1]
        if email_domain in domains:
            return True
        return False
    return True
