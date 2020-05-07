from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from utils.pagination import StandardResultsSetPagination
from .models import EvaluationCommittee
from .models import Team
from .serializers import EvaluationCommitteeSerializer
from .serializers import TeamSerializer


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
    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(teams, request)
        serializer = TeamSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        serializer = TeamSerializer(teams, many=True)
        response = {
            "data": {"teams": serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)
