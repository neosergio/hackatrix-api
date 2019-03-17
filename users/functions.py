import time
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import User


def generate_user_qr_code(user):
    code_base = str(int(time.time()))
    user_qr_code = code_base + str(user.id)
    return user_qr_code


def validate_user_qr_code(code, user):
    user = get_object_or_404(User, pk=code[10:])
    code_extracted = int(code[:10])
    min_value = int(time.time()) - settings.SECONDS_TO_REFRESH_IDENTITY
    if code_extracted >= min_value:
        if code == user.one_time_use_code:
            return True
        else:
            return False
    else:
        return False
