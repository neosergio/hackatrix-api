from django.urls import path

from .views import event_featured
from .views import registrant_list, registrant_qr_code


app_name = 'events'

urlpatterns = [
    path('featured/', event_featured, name='event_featured'),
    path('registrant/list/', registrant_list, name='registrant_list'),
    path('registrant/qr/<str:email>', registrant_qr_code, name='registrant_qr_code'),
]
