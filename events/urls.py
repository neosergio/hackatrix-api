from django.urls import path

from .views import event_register_participant, event_featured

app_name = 'events'

urlpatterns = [
    path('featured/', event_featured, name='event_featured'),
    path('register/participant/<str:code>', event_register_participant, name='event_register_participant'),
]
