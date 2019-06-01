from constance import config
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from assessments.models import ProjectAssessment, RegistrantAssessment
from events.models import Attendance, Registrant, RegistrantAttendance
from ideas.models import IdeaTeamMember, Idea


@login_required()
def index(request):
    return render(request, 'index.html')


@login_required()
def attendance_items(request):
    if config.DISPLAY_REPORTS:
        attendances = Attendance.objects.all()
        context = {'attendances': attendances}
    else:
        context = dict()
    return render(request, 'attendances.html', context)


@login_required()
def attendance_list(request):
    if config.DISPLAY_REPORTS:
        attendances = RegistrantAttendance.objects.all()
        context = {'attendances': attendances}
    else:
        context = dict()
    return render(request, 'attendance_list.html', context)


@login_required()
def attendance_list_by_id(request, attendance_id):
    if config.DISPLAY_REPORTS:
        attendance = get_object_or_404(Attendance, pk=attendance_id)
        attendances = RegistrantAttendance.objects.filter(attendance=attendance)
        context = {'attendances': attendances}
    else:
        context = dict()
    return render(request, 'attendance_list.html', context)


@login_required()
def idea_list(request):
    if config.DISPLAY_REPORTS and config.DISPLAY_PROJECT_REPORTS:
        ideas = Idea.objects.all()
        context = {'ideas': ideas}
    else:
        context = dict()
    return render(request, 'idea_list.html', context)


@login_required()
def project_assessment_by_evaluation_committee(request):
    if config.DISPLAY_REPORTS and config.DISPLAY_PROJECT_REPORTS:
        assessments = ProjectAssessment.objects.all()
        context = {'assessments': assessments}
    else:
        context = dict()
    return render(request, 'project_assessment.html', context)


@login_required()
def project_assessment_by_jury(request):
    if config.DISPLAY_REPORTS and config.DISPLAY_JURY_REPORTS:
        assessments = ProjectAssessment.objects.filter(assessment__is_for_jury=True)
        context = {'assessments': assessments}
    else:
        context = dict()
    return render(request, 'project_assessment.html', context)


@login_required()
def registrant_assessment(request):
    if config.DISPLAY_REPORTS and config.DISPLAY_REGISTRANT_REPORTS:
        assessments = RegistrantAssessment.objects.all()
        context = {'assessments': assessments}
    else:
        context = dict()
    return render(request, 'registrant_assessment.html', context)


@login_required()
def registrant_list(request):
    if config.DISPLAY_REPORTS and config.DISPLAY_REGISTRANT_REPORTS:
        registrants = Registrant.objects.all()
        context = {'registrants': registrants}
    else:
        context = dict()
    return render(request, 'registrant_list.html', context)


@login_required()
def registrant_list_by_project(request):
    if config.DISPLAY_REPORTS and config.DISPLAY_PROJECT_REPORTS:
        teams = IdeaTeamMember.objects.all()
        context = {'teams': teams}
    else:
        context = dict()
    return render(request, 'registrant_list_by_project.html', context)
