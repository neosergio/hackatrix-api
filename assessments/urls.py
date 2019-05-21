from django.urls import path

from .views import project_assessment_list, project_assessment, project_assessment_result
from .views import registrant_assessment_list, registrant_assessment, registrant_assessment_result

app_name = 'assessments'

urlpatterns = [
    path('project/list/', project_assessment_list, name='project_assessment_list'),
    path('project/idea/<int:idea_id>/score/', project_assessment, name='project_assessment'),
    path('project/idea/<int:idea_id>/results/', project_assessment_result, name='project_assessment_result'),
    path('registrant/list/', registrant_assessment_list, name='registrant_assessment_list'),
    path('registrant/<int:registrant_id>/score/', registrant_assessment, name='registrant_assessment'),
    path('registrant/<int:registrant_id>/results/', registrant_assessment_result, name='registrant_assessment_result'),
]
