from django.urls import path

from .views import CustomAuthToken, user_logout, user_create
from .views import user_validation, user_password_recovery_request


app_name = 'users'

urlpatterns = [
    path('authenticate/', CustomAuthToken.as_view()),
    path('create/', user_create, name='user_create'),
    path('logout/', user_logout, name='user_logout'),
    path('validate/<user_uuid>/', user_validation, name='user_validation'),
    path('reset/password/', user_password_recovery_request, name='user_password_recovery_request'),
]
