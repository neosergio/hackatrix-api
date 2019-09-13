from django.shortcuts import get_object_or_404
from itertools import chain
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Assessment, ProjectAssessment, RegistrantAssessment, TeamAssessmentResults, TeamAssessment
from .serializers import AssessmentSerializer, ScoreBulkSerializer, AssessmentResultSerializer
from events.models import Registrant, Team
from ideas.models import Idea
from users.permissions import IsFromHR, IsProjectEvaluator


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


@api_view(['GET', ])
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
