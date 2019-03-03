from django.urls import path

from .views import event_featured_list

app_name = 'events'

urlpatterns = [
    path('featured/list/', event_featured_list, name='event_featured_list'),
]
