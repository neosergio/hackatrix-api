from django.urls import path

from .views import event_featured, registrant_list


app_name = 'events'

urlpatterns = [
    path('featured/', event_featured, name='event_featured'),
    path('registrant/list/', registrant_list, name='registrant_list'),
]
