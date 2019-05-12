from django.urls import path

from .views import idea_creation
from .views import idea_add_team_member, idea_add_team_member_list
from .views import idea_remove_team_member, idea_remove_team_member_list
from .views import idea_detail, idea_list_complete, idea_list_validated
from .views import idea_validation_switch

app_name = 'ideas'

urlpatterns = [
    path('create/', idea_creation, name='idea_creation'),
    path('<int:idea_id>/add/team/member/', idea_add_team_member, name='idea_add_team_member'),
    path('<int:idea_id>/remove/team/member/', idea_remove_team_member, name='idea_remove_team_member'),
    path('<int:idea_id>/add/team/list/', idea_add_team_member_list, name='idea_add_team_member_list'),
    path('<int:idea_id>/remove/team/list/', idea_remove_team_member_list, name='idea_remove_team_member_list'),
    path('<int:idea_id>/detail/', idea_detail, name='idea_detail'),
    path('<int:idea_id>/validation/switch/', idea_validation_switch, name='idea_validation_switch'),
    path('list/complete/', idea_list_complete, name='idea_list_complete'),
    path('list/validated/', idea_list_validated, name='idea_list_validated'),
]
