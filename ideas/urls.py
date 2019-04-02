from django.urls import path

from .views import idea_creation, idea_detail, idea_list_complete

app_name = 'ideas'

urlpatterns = [
    path('creation/', idea_creation, name='idea_creation'),
    path('<int:idea_id>/detail/', idea_detail, name='idea_detail'),
    path('list/complete/', idea_list_complete, name='idea_list_complete'),
]
