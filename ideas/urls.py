from django.urls import path

from .views import idea_detail, idea_list_complete, idea_list_validated
from .views import idea_validation_switch

app_name = 'ideas'

urlpatterns = [
    path('<int:idea_id>/detail/', idea_detail, name='idea_detail'),
    path('<int:idea_id>/validation/switch/', idea_validation_switch, name='idea_validation_switch'),
    path('list/complete/', idea_list_complete, name='idea_list_complete'),
    path('list/validated/', idea_list_validated, name='idea_list_validated'),
]
