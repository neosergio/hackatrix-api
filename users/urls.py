from django.urls import path

from .views import CustomAuthToken
from .views import send_user_evaluator_random_password
from .views import user_create
from .views import user_list
from .views import user_logout
# from .views import user_validation, user_password_recovery_request, user_password_recovery_request_confirmation
from .views import user_password_update
from .views import user_profile
from .views import user_profile_update
from .views import users_active_summary
from .views import user_activation

app_name = 'users'

urlpatterns = [
    path('active/', users_active_summary, name='users_active_summary'),
    path('<int:user_id>/activation/', user_activation, name='user_activation'),
    path('authenticate/', CustomAuthToken.as_view()),
    path('create/', user_create, name='user_create'),
    path('list/', user_list, name='user_list'),
    path('logout/', user_logout, name='user_logout'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/update/', user_profile_update, name='user_profile_update'),
    path('send/password/evaluators/', send_user_evaluator_random_password, name='send_user_evaluator_random_password'),
    # path('reset/password/',
    #     user_password_recovery_request,
    #     name='user_password_recovery_request'),
    # path('reset/password/<uuid:user_uuid>/',
    #     user_password_recovery_request_confirmation,
    #     name='user_password_recovery_request_confirmation'),
    path('update/password/', user_password_update, name='user_password_update'),
    # path('validate/<uuid:user_uuid>/', user_validation, name='user_validation'),
]
