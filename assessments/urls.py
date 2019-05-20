from django.urls import path

from .views import project_assessment_list

app_name = 'assessments'

urlpatterns = [
    path('project/list/', project_assessment_list, name='project_assessment_list'),
]
