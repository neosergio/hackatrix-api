from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from assessments.models import ProjectAssessment
from events.models import RegistrantAttendance


@login_required()
def index(request):
    return render(request, 'index.html')


@login_required()
def attendance_list(request):
    attendances = RegistrantAttendance.objects.all()
    context = {'attendances': attendances}
    return render(request, 'attendance_list.html', context)


@login_required()
def project_assessment(request):
    assessments = ProjectAssessment.objects.all()
    context = {'assessments': assessments}
    return render(request, 'project_assessment.html', context)
