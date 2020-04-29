from django.urls import path

from .views import evaluation_committee_list

app_name = "online"

urlpatterns = [
    path('evaluation/committee/list/', evaluation_committee_list, name="evaluation_committee_list")
]
