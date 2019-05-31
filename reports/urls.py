from django.urls import path

from .views import index, attendance_list, registrant_assessment
from .views import project_assessment_by_jury, project_assessment_by_evaluation_committee


app_name = 'reports'

urlpatterns = [
    path('', index, name='index'),
    path('attendance/list/', attendance_list, name='attendance_list'),
    path('assessment/project/',
         project_assessment_by_evaluation_committee,
         name='project_assessment_by_evaluation_committee'),
    path('assessment/project/by/jury', project_assessment_by_jury, name='project_assessment_by_jury'),
    path('assessment/registrant/', registrant_assessment, name='registrant_assessment'),
]
