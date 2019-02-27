from django.urls import path

from .views import CustomAuthToken, user_logout


urlpatterns = [
    path('authenticate/', CustomAuthToken.as_view()),
    path('logout/', user_logout, name='user_logout'),
]
