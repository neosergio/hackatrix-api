from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from uuid import uuid4

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first_name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, blank=True)
    full_name = models.CharField(max_length=60, blank=True, null=True)
    date_joined = models.DateTimeField(_('date_joined'), auto_now_add=True)

    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_moderator = models.BooleanField(default=False)
    is_team_leader = models.BooleanField(default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_blocked = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)

    is_jury = models.BooleanField(default=False)
    is_from_HR = models.BooleanField(default=False)
    is_from_evaluation_committee = models.BooleanField(default=False)

    is_password_reset_required = models.BooleanField(default=False)
    reset_password_code = models.UUIDField(default=None, blank=True, null=True)
    temporary_password = models.CharField(max_length=4, blank=True, null=True)
    validation_code = models.UUIDField(default=None, blank=True, null=True)
    one_time_use_code = models.CharField(max_length=20, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def generate_reset_password_code(self):
        '''
        Returns UUID string to be sent by email when user require a password recovery action
        '''
        uuid_code = uuid4()
        self.reset_password_code = str(uuid_code)
        self.temporary_password = get_random_string(4, "hacktrx23456789")
        self.save()
        return self.reset_password_code

    def generate_validation_code(self):
        """
        Returns UUID string to be sent by email when user account is created
        """
        uuid_code = uuid4()
        self.validation_code = str(uuid_code)
        self.save()
        return self.validation_code

    def normalize_user_evaluator_role(self):
        """
        Avoids to have multiple roles at the same time: is_jury, is_from_HR, is_from_evaluation_committee
        """
        evaluator_role_counter = 0
        if self.is_jury:
            evaluator_role_counter += 1
        if self.is_from_HR:
            evaluator_role_counter += 1
        if self.is_from_evaluation_committee:
            evaluator_role_counter += 1
        if evaluator_role_counter > 1:
            self.is_jury = False
            self.is_from_HR = False
            self.is_from_evaluation_committee = False

    def save(self, *args, **kwargs):
        self.normalize_user_evaluator_role()
        super().save(*args, **kwargs)


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserDevice(models.Model):
    user = models.ForeignKey(User, related_name='user_device', on_delete=models.CASCADE)
    operating_system = models.CharField(max_length=10)
    code = models.CharField(max_length=200)

    class Meta(object):
        ordering = ['user']
