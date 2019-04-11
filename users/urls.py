from django.urls import path

from .views import CustomAuthToken, user_logout, user_create, user_list
from .views import user_validation, user_password_recovery_request, user_password_recovery_request_confirmation
from .views import user_password_update, user_profile, user_profile_update
from .views import user_identity, user_identity_validation


app_name = 'users'

urlpatterns = [
    path('authenticate/', CustomAuthToken.as_view()),
    path('create/', user_create, name='user_create'),
    path('identity/', user_identity, name='user_identity'),
    path('identity/validation/', user_identity_validation, name='user_identity_validation'),
    path('list/', user_list, name='user_list'),
    path('logout/', user_logout, name='user_logout'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/update/', user_profile_update, name='user_profile_update'),
    path('reset/password/',
         user_password_recovery_request,
         name='user_password_recovery_request'),
    path('reset/password/<uuid:user_uuid>/',
         user_password_recovery_request_confirmation,
         name='user_password_recovery_request_confirmation'),
    path('update/password/', user_password_update, name='user_password_update'),
    path('validate/<uuid:user_uuid>/', user_validation, name='user_validation'),
]
