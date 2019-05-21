from django.urls import path

from .views import project_assessment_list, project_assessment

app_name = 'assessments'

urlpatterns = [
    path('project/list/', project_assessment_list, name='project_assessment_list'),
    path('project/idea/<int:idea_id>/score/', project_assessment, name='project_assessment'),
]
