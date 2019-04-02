from django.urls import path

from .views import event_register_participant, event_featured
from .views import event_sent_participant_codes

app_name = 'events'

urlpatterns = [
    path('featured/', event_featured, name='event_featured'),
    path('featured/participant/sent/code/', event_sent_participant_codes, name='event_sent_participant_codes'),
    path('register/participant/<str:code>', event_register_participant, name='event_register_participant'),
]
