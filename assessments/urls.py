from django.urls import path

from .views import project_assessment_list, project_assessment, project_assessment_result
from .views import registrant_assessment_list, registrant_assessment, registrant_assessment_result
from .views import team_assessment, team_assessment_complete

app_name = 'assessments'

urlpatterns = [
    path('project/list/', project_assessment_list, name='project_assessment_list'),
    path('project/idea/<int:idea_id>/score/', project_assessment, name='project_assessment'),
    path('project/idea/<int:idea_id>/results/', project_assessment_result, name='project_assessment_result'),
    path('registrant/list/', registrant_assessment_list, name='registrant_assessment_list'),
    path('registrant/<int:registrant_id>/score/', registrant_assessment, name='registrant_assessment'),
    path('registrant/<int:registrant_id>/results/', registrant_assessment_result, name='registrant_assessment_result'),
    path('team/<int:team_id>/score/', team_assessment, name='team_assessment'),
    path('team/<int:team_id>/score/complete/', team_assessment_complete, name='team_assessment_complete'),
]
