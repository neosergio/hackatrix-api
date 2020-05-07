from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from utils.pagination import StandardResultsSetPagination
from .models import EvaluationCommittee
from .models import Team
from .models import TeamMember
from .serializers import EvaluationCommitteeSerializer
from .serializers import TeamMemberCreationSerializer
from .serializers import TeamMemberSerializer


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
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def team_list(request):
    teams = Team.objects.all()
    teams_response = list()
    for team in teams:
        team_members = len(Team.objects.filter(member__team=team))

        if team.evaluation_committee:
            evaluation_committee = team.evaluation_committee.name
        else:
            evaluation_committee = ""

        teams_response.append(
            {"id": team.pk,
             "name": team.name,
             "team_members": team_members,
             "evaluation_committee": evaluation_committee,
             "jury_score": team.jury_score,
             "committee_score": team.committee_score}
        )
    response = {
        "data": {"teams": teams_response}
    }
    return Response(response, status=status.HTTP_200_OK)


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
        return Response(response, status=status.HTTP_202_ACCEPTED)
