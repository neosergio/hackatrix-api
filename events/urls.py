from django.urls import path

from .views import event_register_participant, event_featured
from .views import event_send_participant_codes, event_featured_reset_participants
from .views import event_featured_send_notification

app_name = 'events'

urlpatterns = [
    path('featured/', event_featured, name='event_featured'),
    path('featured/participant/send/code/', event_send_participant_codes, name='event_send_participant_codes'),
    path('featured/participant/send/notification/',
         event_featured_send_notification,
         name='event_featured_send_notification'),
    path('featured/participant/reset/', event_featured_reset_participants, name='event_featured_reset_participants'),
    path('register/participant/<str:code>', event_register_participant, name='event_register_participant'),
]
