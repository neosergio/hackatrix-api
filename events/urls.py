from django.urls import path

from .views import event_featured, event_attendance_list, event_attendance_register
from .views import registrant_list, registrant_qr_code, registrant_identity_validation
from .views import registrant_send_qr_code, registrant_email_sent_flag_to_false
from .views import team_detail, team_list_event_featured, team_update, team_deactivate


app_name = 'events'

urlpatterns = [
    path('featured/', event_featured, name='event_featured'),
    path('featured/attendance/list/', event_attendance_list, name='event_attendance_list'),
    path('featured/attendance/<int:attendance_id>/register/',
         event_attendance_register,
         name='event_attendance_register'),
    path('featured/team/list/', team_list_event_featured, name='team_list_event_featured'),
    path('registrant/list/', registrant_list, name='registrant_list'),
    path('registrant/qr/<str:email>', registrant_qr_code, name='registrant_qr_code'),
    path('registrant/qr/send/', registrant_send_qr_code, name='registrant_send_qr_code'),
    path('registrant/validation/', registrant_identity_validation, name='registrant_identity_validation'),
    path('registrant/list/email_sent_flag/to/false',
         registrant_email_sent_flag_to_false,
         name='registrant_email_sent_flag_to_false'),
    path('team/<int:team_id>/', team_detail, name='team_detail'),
    path('team/<int:team_id>/update/', team_update, name='team_update'),
    path('team/<int:team_id>/deactivate/', team_deactivate, name='team_deactivate'),
]
