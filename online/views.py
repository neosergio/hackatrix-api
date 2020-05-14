from django.db.models import Count
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from users.models import User
from utils.pagination import StandardResultsSetPagination
from .models import CategoryScore
from .models import Evaluation
from .models import EvaluationCommittee
from .models import Evaluator
from .models import Team
from .models import TeamMember
from .permissions import IsEvaluator
from .serializers import EvaluationCommitteeSerializer
from .serializers import EvaluationSaveSerializer
from .serializers import EvaluatorCommitteeSerializer
from .serializers import ScoreSerializer
from .serializers import TeamCreationSerializer
from .serializers import TeamMemberCreationSerializer
from .serializers import TeamMemberSaveSerializer
from .serializers import TeamMemberSerializer
from .serializers import TeamUpdateSerializer
from .serializers import UserCommitteesSerializer


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def evaluated_teams(request):
    total_teams = Team.objects.all().count()
    committee_evaluations_grouped_by_teams = Team.objects.filter(
        evaluation__category_score__is_committee_score=True).annotate(num_evaluations=Count('evaluation')).count()
    jury_evaluations_grouped_by_teams = Team.objects.filter(
        evaluation__category_score__is_committee_score=False).annotate(num_evaluations=Count('evaluation')).count()
    response = {"data": {"evaluated_by_committee": committee_evaluations_grouped_by_teams,
                         "evaluated_by_jury": jury_evaluations_grouped_by_teams,
                         "total": total_teams}}
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH'])
@permission_classes((permissions.IsAdminUser, ))
def evaluator_committee(request, user_id):
    evaluator = get_object_or_404(Evaluator, user__pk=user_id)
    if request.method == 'GET':
        response = {"data": {"committee_id": evaluator.evaluation_committee.pk}}
        return Response(response, status=status.HTTP_200_OK)
    if request.method == 'PATCH':
        serializer = EvaluatorCommitteeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            evaluation_committee = get_object_or_404(EvaluationCommittee,
                                                     pk=serializer.validated_data.get('committee_id'))
            evaluator.evaluation_committee = evaluation_committee
            evaluator.save()
            return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def evaluation_committee_list(request):
    committees = EvaluationCommittee.objects.all()
    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(committees, request)
        serializer = EvaluationCommitteeSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        serializer = EvaluationCommitteeSerializer(committees, many=True)
        response = {"data": {"committees": serializer.data}}
        return Response(response, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsEvaluator, ))
def evaluation_save(request):
    serializer = EvaluationSaveSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        evaluator = get_object_or_404(Evaluator, user=request.user)
        if evaluator.user.is_jury:
            is_committee_score = False
        else:
            is_committee_score = True
        team_id = serializer.validated_data.get('team_id')
        team = get_object_or_404(Team, pk=team_id)
        scores = serializer.validated_data.get('scores')
        evaluation, created = Evaluation.objects.get_or_create(user=evaluator, team=team)
        for score in scores:
            score_name = score.get('name')
            score_percentage = score.get('percentage')
            score_value = score.get('score')
            CategoryScore.objects.create(
                name=score_name,
                percentage=score_percentage,
                is_committee_score=is_committee_score,
                score=score_value,
                evaluation=evaluation)
        return Response(status=status.HTTP_201_CREATED)


@api_view(['POST', ])
@permission_classes((permissions.IsAdminUser, ))
def team_creation(request):
    serializer = TeamCreationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        name = serializer.validated_data.get('name')
        project = serializer.validated_data.get('project')
        project_description = serializer.validated_data.get('project_description')
        Team.objects.create(name=name, project=project, project_description=project_description)
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team_members = TeamMember.objects.filter(team=team)
    team_members_serializer = TeamMemberSerializer(team_members, many=True)

    if team.evaluation_committee:
        evaluation_committee = team.evaluation_committee.name
    else:
        evaluation_committee = ""

    committee_scores = CategoryScore.objects.filter(is_committee_score=True)
    committee_scores_serializer = ScoreSerializer(committee_scores, many=True)
    jury_scores = CategoryScore.objects.filter(is_committee_score=False)
    jury_scores_serializer = ScoreSerializer(jury_scores, many=True)
    data = {
        "id": team.pk,
        "name": team.name,
        "project": team.project,
        "project_description": team.project_description,
        "evaluation_committee": evaluation_committee,
        "team_members": team_members_serializer.data,
        "committee_scores": committee_scores_serializer.data,
        "jury_scores": jury_scores_serializer.data
    }
    response = {'data': data}
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def team_list(request):
    if request.GET.get('search'):
        request_terms = request.GET.get('search')
        search_terms_array = request_terms.split()

        initial_term = search_terms_array[0]
        teams = Team.objects.filter(
            Q(name__icontains=initial_term) |
            Q(project__icontains=initial_term) |
            Q(project_description__icontains=initial_term))
        if len(search_terms_array) > 1:
            for term in range(1, len(search_terms_array)):
                teams = teams.filter(
                    Q(name__icontains=term) |
                    Q(project__icontains=term) |
                    Q(project_description__icontains=term))
    else:
        teams = Team.objects.all()

    teams_response = list()
    for team in teams:
        team_members = len(Team.objects.filter(member__team=team))

        if team.evaluation_committee:
            evaluation_committee = team.evaluation_committee.name
        else:
            evaluation_committee = ""

        jury_score = len(CategoryScore.objects.filter(is_committee_score=False, evaluation__team=team))
        committee_score = len(CategoryScore.objects.filter(is_committee_score=True, evaluation__team=team))

        teams_response.append(
            {"id": team.pk,
             "name": team.name,
             "team_members": team_members,
             "evaluation_committee": evaluation_committee,
             "jury_score": jury_score,
             "committee_score": committee_score}
        )
    response = {
        "data": {"teams": teams_response}
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAdminUser, ))
def team_member(request):
    if request.method == 'POST':
        serializer = TeamMemberSaveSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            team = get_object_or_404(Team, pk=serializer.validated_data.get('team_id'))
            team_members = TeamMember.objects.filter(team=team)
            team_members.delete()
            members = serializer.validated_data.get('members')
            if len(members) > 0:
                for member in members:
                    name = member.get('name')
                    surname = member.get('surname')
                    email = member.get('email')
                    TeamMember.objects.create(
                        name=name,
                        surname=surname,
                        email=email,
                        team=team)
            return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((permissions.IsAdminUser, ))
def team_member_creation(request):
    serializer = TeamMemberCreationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        name = serializer.validated_data.get('name')
        surname = serializer.validated_data.get('surname')
        email = serializer.validated_data.get('email')
        team = get_object_or_404(Team, pk=serializer.validated_data.get('team'))
        team_member = TeamMember.objects.create(
            name=name,
            surname=surname,
            email=email,
            team=team
        )
        response_serializer = TeamMemberSerializer(team_member)
        response = {'data': response_serializer.data}
        return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
@permission_classes((IsEvaluator, ))
def team_list_to_evaluate(request):
    evaluator = get_object_or_404(Evaluator, user=request.user)
    committee = evaluator.evaluation_committee
    teams_response = list()
    teams = Team.objects.filter(evaluation_committee=committee)
    for team in teams:
        team_member_list_count = len(TeamMember.objects.filter(team=team))
        scores = list()
        total_score = 0
        if evaluator.user.is_from_evaluation_committee:
            scores = CategoryScore.objects.filter(is_committee_score=True, evaluation__team=team)
        if evaluator.user.is_jury:
            scores = CategoryScore.objects.filter(is_committee_score=False, evaluation__team=team)
        if len(scores) > 0:
            for score in scores:
                total_score += (score.score * score.percentage)

        teams_response.append(
            {"id": team.pk,
             "name": team.name,
             "team_members": team_member_list_count,
             "score": total_score}
        )
    response = {
        "data": {"Teams": teams_response}
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((permissions.IsAdminUser, ))
def team_update(request):
    serializer = TeamUpdateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        team = get_object_or_404(Team, pk=serializer.validated_data.get('id'))
        team.name = serializer.validated_data.get('name')
        team.project = serializer.validated_data.get('project')
        team.project_description = serializer.validated_data.get('project_description')
        team.save()
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((IsEvaluator, ))
def team_to_evaluate(request, team_id):
    evaluator = get_object_or_404(Evaluator, user=request.user)
    team = get_object_or_404(Team, pk=team_id)
    team_members = TeamMember.objects.filter(team=team)
    team_members_serializer = TeamMemberSerializer(team_members, many=True)
    evaluation = Evaluation.objects.filter(user=evaluator, team=team)
    if len(evaluation) > 0:
        evaluation = evaluation[0]
        scores = CategoryScore.objects.filter(evaluation=evaluation)
        scores_serializer = ScoreSerializer(scores, many=True)
        scores_data = scores_serializer.data
    else:
        scores_data = None
    data = {
        "id": team.pk,
        "name": team.name,
        "project": team.project,
        "project_description": team.project_description,
        "team_members": team_members_serializer.data,
        "scores": scores_data
    }
    response = {'data': data}
    return Response(response, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((permissions.IsAdminUser, ))
def set_users_committees(request):
    serializer = UserCommitteesSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        committee = get_object_or_404(EvaluationCommittee, pk=serializer.validated_data.get('committee_id'))
        evaluators = Evaluator.objects.filter(evaluation_committee=committee)
        evaluators.delete()
        users = serializer.validated_data.get('users')
        if len(users) > 0:
            for user in users:
                user = get_object_or_404(User, pk=user.get('user_id'))
                Evaluator.objects.create(user=user, evaluation_committee=committee)
        return Response(status=status.HTTP_202_ACCEPTED)
