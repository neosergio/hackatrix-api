from django.urls import path

from .views import idea_creation, idea_detail

app_name = 'ideas'

urlpatterns = [
    path('creation/', idea_creation, name='idea_creation'),
    path('<int:idea_id>/detail/', idea_detail, name='idea_detail'),
]
