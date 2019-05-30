from django.urls import path

from .views import index, attendance_list, project_assessment


app_name = 'reports'

urlpatterns = [
    path('', index, name='index'),
    path('attendance/list/', attendance_list, name='attendance_list'),
    path('assessment/project/', project_assessment, name='project_assessment'),
]
