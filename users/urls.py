from django.urls import path

from .views import CustomAuthToken


urlpatterns = [
    path('authenticate/', CustomAuthToken.as_view()),
]
