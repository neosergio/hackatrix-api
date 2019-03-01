from django.urls import path

from .views import CustomAuthToken, user_logout, user_create
from .views import user_validation, user_password_recovery_request, user_password_recovery_request_confirmation
from .views import user_password_update


app_name = 'users'

urlpatterns = [
    path('authenticate/', CustomAuthToken.as_view()),
    path('create/', user_create, name='user_create'),
    path('logout/', user_logout, name='user_logout'),
    path('reset/password/',
         user_password_recovery_request,
         name='user_password_recovery_request'),
    path('reset/password/<user_uuid>/',
         user_password_recovery_request_confirmation,
         name='user_password_recovery_request_confirmation'),
    path('update/password/', user_password_update, name='user_password_update'),
    path('validate/<user_uuid>/', user_validation, name='user_validation'),
]
