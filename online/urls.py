from django.urls import path

from .views import evaluation_committee_list
from .views import team_list

app_name = "online"

urlpatterns = [
    path('evaluation/committee/list/', evaluation_committee_list, name="evaluation_committee_list"),
    path('team/list/', team_list, name="team_list")
]
