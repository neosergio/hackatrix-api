from django.urls import path

from .views import event_featured, registrant_list
from .views import event_send_participant_codes
from .views import event_featured_send_notification

app_name = 'events'

urlpatterns = [
    path('featured/', event_featured, name='event_featured'),
    path('featured/participant/send/code/', event_send_participant_codes, name='event_send_participant_codes'),
    path('featured/participant/send/notification/',
         event_featured_send_notification,
         name='event_featured_send_notification'),
    path('registrant/list/', registrant_list, name='registrant_list'),
]
