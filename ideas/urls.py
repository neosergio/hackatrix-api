from django.urls import path

from .views import idea_detail

app_name = 'ideas'

urlpatterns = [
    path('<int:idea_id>/detail/', idea_detail, name='idea_detail'),
]
