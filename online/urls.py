from django.urls import path

from .views import evaluation_committee_list
from .views import team_detail
from .views import team_list
from .views import team_member_creation

app_name = "online"

urlpatterns = [
    path('evaluation/committee/list/', evaluation_committee_list, name="evaluation_committee_list"),
    path('team/<int:team_id>/', team_detail, name="team_detail"),
    path('team/list/', team_list, name="team_list"),
    path('team/member/creation/', team_member_creation, name="team_member_creation")
]
