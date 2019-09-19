from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404
from itertools import chain
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Assessment, ProjectAssessment, RegistrantAssessment
from .models import TeamAssessmentResults, TeamAssessment, FinalResult
from .serializers import AssessmentSerializer, ScoreBulkSerializer, AssessmentResultSerializer
from .serializers import FinalResultSerializer
from events.models import Registrant, Team, Event
from ideas.models import Idea
from users.models import User
from users.permissions import IsFromHR, IsProjectEvaluator, IsModerator


@api_view(['GET', ])
@permission_classes((IsProjectEvaluator, ))
def project_assessment_list(request):
    """
    Returns assessment list by user
    """
    user = request.user
    return_list = list()

    if user.is_from_evaluation_committee:
        committee_assessments = Assessment.objects.filter(is_for_evaluation_committee=True)
        return_list = list(chain(return_list, committee_assessments))

    if user.is_jury:
        jury_assessments = Assessment.objects.filter(is_for_jury=True)
        return_list = list(chain(return_list, jury_assessments))

    serializer = AssessmentSerializer(return_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsProjectEvaluator, ))
def project_assessment(request, idea_id):
    """
    Assigns score to a project assessment criteria
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    evaluator = request.user
    serializer = ScoreBulkSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        score_list = serializer.validated_data['score_list']
        for score in score_list:
            try:
                assessment = Assessment.objects.get(pk=score['assessment_id'])
                ProjectAssessment.objects.create(
                    assessment=assessment,
                    idea=idea,
                    evaluator=evaluator,
                    value=score['value'])
            except Exception as e:
                print(e)
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((IsProjectEvaluator, ))
def project_assessment_result(request, idea_id):
    """
    Returns project scores
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    evaluator = request.user
    results = ProjectAssessment.objects.filter(idea=idea, evaluator=evaluator)
    serializer = AssessmentResultSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((IsFromHR, ))
def registrant_assessment_list(request):
    """
    Returns assessment list by user
    """
    user = request.user

    if user.is_from_HR:
        assessments = Assessment.objects.filter(is_for_HR=True)
        serializer = AssessmentSerializer(assessments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsFromHR, ))
def registrant_assessment(request, registrant_id):
    registrant = get_object_or_404(Registrant, pk=registrant_id)
    evaluator = request.user
    serializer = ScoreBulkSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        score_list = serializer.validated_data['score_list']
        for score in score_list:
            try:
                assessment = Assessment.objects.get(pk=score['assessment_id'])
                RegistrantAssessment.objects.create(
                    assessment=assessment,
                    registrant=registrant,
                    evaluator=evaluator,
                    value=score['value'])
            except Exception as e:
                print(e)
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((IsProjectEvaluator, ))
def registrant_assessment_result(request, registrant_id):
    """
    Returns project scores
    """
    registrant = get_object_or_404(Registrant, pk=registrant_id)
    evaluator = request.user
    results = RegistrantAssessment.objects.filter(registrant=registrant, evaluator=evaluator)
    serializer = AssessmentResultSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((IsProjectEvaluator, ))
def team_assessment(request, team_id):
    """
    Assigns score to a team assessment criteria
    """
    team = get_object_or_404(Team, pk=team_id)
    evaluator = request.user
    serializer = ScoreBulkSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        score_list = serializer.validated_data['score_list']
        for score in score_list:
            try:
                assessment = Assessment.objects.get(pk=score['assessment_id'])
                TeamAssessmentResults.objects.create(
                    assessment=assessment,
                    team=team,
                    evaluator=evaluator,
                    value=score['value'])
            except Exception as e:
                print(e)
        TeamAssessment.objects.create(team=team, evaluator=evaluator, has_been_assessed=True)
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH', ])
@permission_classes((IsProjectEvaluator, ))
def team_assessment_complete(request, team_id):
    """
    Marks as assessment team complete
    """
    team = get_object_or_404(Team, pk=team_id)
    evaluator = request.user
    assessment = get_object_or_404(TeamAssessment, team=team, evaluator=evaluator)
    assessment.has_been_assessed = True
    assessment.save()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((IsModerator, ))
def team_assessment_results_calculate(request):
    """
    Returns team assessments results
    """
    teams_response = list()
    assessment_type = ''
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    teams = Team.objects.filter(event=event, is_active=True, is_valid=True)
    FinalResult.objects.all().delete()
    is_completed = False

    for team in teams:
        if request.GET.get('role'):
            if request.GET.get('role') == 'committee':
                assessments_total_sum = TeamAssessmentResults.objects.filter(
                    team=team,
                    assessment__is_for_evaluation_committee=True).aggregate(Sum('value'))
                assessment_type = 'committee'
            elif request.GET.get('role') == 'jury':
                assessments_total_sum = TeamAssessmentResults.objects.filter(
                    team=team,
                    assessment__is_for_jury=True).aggregate(Sum('value'))
                assessment_type = 'jury'
        else:
            assessments_total_sum = TeamAssessmentResults.objects.filter(team=team).aggregate(Sum('value'))
            assessment_type = 'general'
        teams_response.append({'id': team.pk,
                               'title': team.title,
                               'score': assessments_total_sum['value__sum'],
                               'type': assessment_type})
        FinalResult.objects.create(team=team, score=assessments_total_sum['value__sum'], type=type)

    # Check if assessments are completed.
    teams_count = len(Team.objects.filter(is_active=True, is_valid=True, event=event))

    if request.GET.get('role') and request.GET.get('role') == 'committee':
        assessment_criteria = Assessment.objects.filter(is_for_evaluation_committee=True)
        evaluators = User.objects.filter(is_active=True, is_from_evaluation_committee=True)
        assessments = TeamAssessmentResults.objects.filter(assessment__is_for_evaluation_committee=True)
    elif request.GET.get('role') and request.GET.get('role') == 'jury':
        assessment_criteria = Assessment.objects.filter(is_for_jury=True)
        evaluators = User.objects.filter(is_active=True, is_jury=True)
        assessments = TeamAssessmentResults.objects.filter(assessment__is_for_jury=True)
    else:
        assessment_criteria = Assessment.objects.all()
        evaluators = User.objects.filter(Q(is_jury=True) | Q(is_from_evaluation_committee=True))
        assessments = TeamAssessmentResults.objects.all()

    assessment_criteria_count = len(assessment_criteria)
    evaluators_count = len(evaluators)
    assessments_count = len(assessments)
    total_expected_assessments = teams_count * assessment_criteria_count * evaluators_count

    if assessments_count == total_expected_assessments:
        is_completed = True
    else:
        is_completed = False

    response = {'is_completed': is_completed,
                'teams': teams_response}

    return Response(response, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((IsModerator, ))
def team_assessments_result(request):
    """
    Returns team assessments final results
    """
    if request.GET.get('type') and request.GET.get('type') == 'committee':
        results = FinalResult.objects.filter(type='committee')
        serializer = FinalResultSerializer(results, many=True)
    elif request.GET.get('type') and request.GET.get('type') == 'jury':
        result = FinalResult.objects.filter(type='jury').latest('score')
        serializer = FinalResultSerializer(result)
    else:
        results = FinalResult.objects.all()
        serializer = FinalResultSerializer(results, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
