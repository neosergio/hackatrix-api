from django.urls import path

from .views import CustomAuthToken, user_logout, user_create


urlpatterns = [
    path('authenticate/', CustomAuthToken.as_view()),
    path('create/', user_create, name='user_create'),
    path('logout/', user_logout, name='user_logout'),
]
