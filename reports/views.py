from django.shortcuts import render

from events.models import RegistrantAttendance


def index(request):
    return render(request, 'index.html')


def attendance_list(request):
    attendances = RegistrantAttendance.objects.all()
    context = {'attendances': attendances}
    return render(request, 'attendance_list.html', context)
