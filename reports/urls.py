from django.urls import path

from .views import index, attendance_list, attendance_list_by_id, attendance_items
from .views import project_assessment_by_jury, project_assessment_by_evaluation_committee, idea_list
from .views import registrant_list_by_project, registrant_assessment, registrant_list


app_name = 'reports'

urlpatterns = [
    path('', index, name='index'),
    path('attendance/', attendance_items, name='attendance_items'),
    path('attendance/<int:attendance_id>/list/', attendance_list_by_id, name='attendance_list_by_id'),
    path('attendance/list/', attendance_list, name='attendance_list'),
    path('project/list/', idea_list, name='idea_list'),
    path('project/teams/', registrant_list_by_project, name='registrant_list_by_project'),
    path('registrant/list/', registrant_list, name='registrant_list'),
    path('assessment/project/',
         project_assessment_by_evaluation_committee,
         name='project_assessment_by_evaluation_committee'),
    path('assessment/project/by/jury', project_assessment_by_jury, name='project_assessment_by_jury'),
    path('assessment/registrant/', registrant_assessment, name='registrant_assessment'),
]
