from django.urls import path

from .views import event_featured_list, event_register_participant, event_detail

app_name = 'events'

urlpatterns = [
    path('<int:event_id>/detail/', event_detail, name='event_detail'),
    path('featured/list/', event_featured_list, name='event_featured_list'),
    path('register/participant/<str:code>', event_register_participant, name='event_register_participant'),
]
