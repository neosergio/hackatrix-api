from django.urls import path

from .views import index, attendance_list, attendance_list_by_id, attendance_items
from .views import project_assessment_by_jury, project_assessment_by_evaluation_committee, idea_list
from .views import registrant_list_by_project, registrant_assessment, registrant_list
from .views import team_list, team_member_list
from .views import team_assessment, final_results
from .views import get_qr_code_by_email


app_name = 'reports'

urlpatterns = [
    path('', index, name='index'),
    path('attendance/', attendance_items, name='attendance_items'),
    path('attendance/<int:attendance_id>/list/', attendance_list_by_id, name='attendance_list_by_id'),
    path('attendance/list/', attendance_list, name='attendance_list'),
    path('project/list/', idea_list, name='idea_list'),
    path('team/list/', team_list, name='team_list'),
    path('team/member/list/', team_member_list, name='team_member_list'),
    path('project/teams/', registrant_list_by_project, name='registrant_list_by_project'),
    path('registrant/list/', registrant_list, name='registrant_list'),
    path('registrant/QR/', get_qr_code_by_email, name='get_qr_code_by_email'),
    path('assessment/project/',
         project_assessment_by_evaluation_committee,
         name='project_assessment_by_evaluation_committee'),
    path('assessment/team/', team_assessment, name='team_assessment'),
    path('assessment/project/by/jury', project_assessment_by_jury, name='project_assessment_by_jury'),
    path('assessment/registrant/', registrant_assessment, name='registrant_assessment'),
    path('final/results/', final_results, name='final_results'),
]
