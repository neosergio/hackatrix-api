from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from import_export.admin import ImportExportMixin

from .models import User, UserDevice


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password using "
                                                    "<a href=\'../password/\'>this form</a>."))

    class Meta():
        model = User
        fields = ('email',)

    def clean_password(self):
        return self.initial['password']


class UserCustomAdmin(ImportExportMixin, BaseUserAdmin):
    form = UserChangeForm
    list_display = ("email",
                    "full_name",
                    "is_staff",
                    "is_moderator",
                    "is_jury",
                    "is_from_HR",
                    "is_from_evaluation_committee")
    search_fields = ['email', 'full_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name',
                                      'last_name',
                                      'full_name')}),
        ('Permissions', {'fields': ('is_superuser',
                                    'is_staff',
                                    'is_moderator',
                                    'is_team_leader',
                                    'is_active',
                                    'is_blocked',
                                    'is_validated',
                                    'groups',
                                    'user_permissions')}),
        ('Evaluator', {'fields': ('is_jury',
                                  'is_from_HR',
                                  'is_from_evaluation_committee')}),
        ('Security options', {'fields': ('is_password_reset_required',
                                         'reset_password_code',
                                         'temporary_password',
                                         'validation_code')}),
        ('History', {'fields': ('date_joined', 'last_login')})
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('date_joined',)
    ordering = ('email',)


class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'operating_system', 'code')


admin.site.register(User, UserCustomAdmin)
admin.site.register(UserDevice, UserDeviceAdmin)
