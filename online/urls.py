from django.urls import path

from .views import evaluation_committee_list
from .views import evaluation_save
from .views import team_detail
from .views import team_list
from .views import team_list_to_evaluate
from .views import team_member
from .views import team_member_creation
from .views import team_to_evaluate

app_name = "online"

urlpatterns = [
    path('evaluation/save/', evaluation_save, name="evaluation_save"),
    path('evaluation/committee/list/', evaluation_committee_list, name="evaluation_committee_list"),
    path('team/<int:team_id>/', team_detail, name="team_detail"),
    path('team/<int:team_id>/evaluate/', team_to_evaluate, name="team_to_evaluate"),
    path('team/list/', team_list, name="team_list"),
    path('team/list/evaluate/', team_list_to_evaluate, name="team_list_to_evaluate"),
    path('team/member/', team_member, name="team_member"),
    path('team/member/creation/', team_member_creation, name="team_member_creation")
]
