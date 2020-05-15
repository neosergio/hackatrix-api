from django.urls import path

from .views import evaluated_teams
from .views import evaluation_committee_creation
from .views import evaluation_committee_update
from .views import evaluation_committee_list
from .views import evaluation_save
from .views import evaluator_committee
from .views import set_teams_committees
from .views import set_users_committees
from .views import team_creation
from .views import team_detail
from .views import team_disqualify
from .views import team_list
from .views import team_list_to_evaluate
from .views import team_member
from .views import team_member_creation
from .views import team_to_evaluate
from .views import team_update

app_name = "online"

urlpatterns = [
    path('evaluator/<int:user_id>/committee/', evaluator_committee, name="evaluator_committee"),
    path('evaluation/committee/create/', evaluation_committee_creation, name="evaluation_committee_creation"),
    path('evaluation/committee/update/', evaluation_committee_update, name="evaluation_committee_update"),
    path('evaluation/committee/list/', evaluation_committee_list, name="evaluation_committee_list"),
    path('evaluation/committee/evaluators/', set_users_committees, name="set_users_committees"),
    path('evaluation/committee/teams/', set_teams_committees, name="set_teams_committees"),
    path('evaluation/save/', evaluation_save, name="evaluation_save"),
    path('evaluation/summary/', evaluated_teams, name="evaluated_teams"),
    path('team/<int:team_id>/', team_detail, name="team_detail"),
    path('team/<int:team_id>/disqualify/', team_disqualify, name="team_disqualify"),
    path('team/<int:team_id>/evaluate/', team_to_evaluate, name="team_to_evaluate"),
    path('team/create/', team_creation, name="team_creation"),
    path('team/list/', team_list, name="team_list"),
    path('team/list/evaluate/', team_list_to_evaluate, name="team_list_to_evaluate"),
    path('team/member/', team_member, name="team_member"),
    path('team/member/creation/', team_member_creation, name="team_member_creation"),
    path('team/update/', team_update, name="team_update"),
]
