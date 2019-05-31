from constance import config
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from assessments.models import ProjectAssessment, RegistrantAssessment
from events.models import RegistrantAttendance
from ideas.models import IdeaTeamMember, Idea


@login_required()
def index(request):
    return render(request, 'index.html')


@login_required()
def attendance_list(request):
    if config.DISPLAY_REPORTS:
        attendances = RegistrantAttendance.objects.all()
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
def registrant_list_by_project(request):
    if config.DISPLAY_REPORTS and config.DISPLAY_PROJECT_REPORTS:
        teams = IdeaTeamMember.objects.all()
        context = {'teams': teams}
    else:
        context = dict()
    return render(request, 'registrant_list_by_project.html', context)
