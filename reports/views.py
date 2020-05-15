from constance import config
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import EmailForm
from assessments.models import ProjectAssessment, RegistrantAssessment, TeamAssessmentResults, FinalResult
from events.models import Attendance, Registrant, RegistrantAttendance, Event, Team, TeamMember
from ideas.models import IdeaTeamMember, Idea


@login_required()
def index(request):
    return render(request, 'index.html')


@login_required()
def attendance_items(request):
    if config.DISPLAY_REPORTS:
        event = Event.objects.filter(is_active=True, is_featured=True).first()
        attendances = Attendance.objects.filter(event=event)
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
def get_qr_code_by_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            registrant = get_object_or_404(Registrant, email=email)
            context = {'form': form,
                       'registrant_code': registrant.code,
                       'qr_code_create_api_url': settings.QR_CODE_CREATE_API_URL}
    else:
        form = EmailForm()
        context = {'form': form}
    return render(request, 'get_qr_code.html', context)


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
        event = Event.objects.filter(is_active=True, is_featured=True).first()
        registrants = Registrant.objects.filter(event=event)
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


@login_required()
def team_list(request):
    context = dict()
    if config.DISPLAY_REPORTS and config.DISPLAY_PROJECT_REPORTS:
        event = Event.objects.filter(is_active=True, is_featured=True).first()
        teams = Team.objects.filter(event=event)
        context = {'teams': teams}
    return render(request, 'team_list.html', context)


@login_required()
def team_member_list(request):
    context = dict()
    if config.DISPLAY_REPORTS and config.DISPLAY_PROJECT_REPORTS:
        event = Event.objects.filter(is_active=True, is_featured=True).first()
        team_members = TeamMember.objects.filter(team__event=event, is_active=True)
        context = {'team_members': team_members}
    return render(request, 'team_member_list.html', context)


@login_required()
def team_assessment(request):
    context = dict()
    if config.DISPLAY_REPORTS and config.DISPLAY_JURY_REPORTS:
        event = Event.objects.filter(is_active=True, is_featured=True).first()
        if request.GET.get('role') and request.GET.get('role') == 'committee':
            assessments = TeamAssessmentResults.objects.filter(
                assessment__is_for_evaluation_committee=True,
                team__event=event)
        elif request.GET.get('role') and request.GET.get('role') == 'jury':
            assessments = TeamAssessmentResults.objects.filter(
                assessment__is_for_jury=True,
                team__event=event)
        else:
            assessments = TeamAssessmentResults.objects.filter(team__event=event)
        context = {'assessments': assessments}
    return render(request, 'team_assessment.html', context)


@login_required()
def final_results(request):
    context = dict()
    if config.DISPLAY_REPORTS and config.DISPLAY_JURY_REPORTS:
        event = Event.objects.filter(is_active=True, is_featured=True).first()
        if request.GET.get('role') and request.GET.get('role') == 'committee':
            results = FinalResult.objects.filter(type='committee', team__event=event)
        elif request.GET.get('role') and request.GET.get('role') == 'jury':
            results = FinalResult.objects.filter(type='jury', team__event=event)
        else:
            results = FinalResult.objects.filter(type='general', team__event=event)
        context = {'results': results}
    return render(request, 'final_results.html', context)
