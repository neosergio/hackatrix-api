from django.urls import path

from .views import event_register_participant, event_featured
from .views import event_sent_participant_codes, event_featured_reset_participants

app_name = 'events'

urlpatterns = [
    path('featured/', event_featured, name='event_featured'),
    path('featured/participant/sent/code/', event_sent_participant_codes, name='event_sent_participant_codes'),
    path('featured/participant/reset/', event_featured_reset_participants, name='event_featured_reset_participants'),
    path('register/participant/<str:code>', event_register_participant, name='event_register_participant'),
]
