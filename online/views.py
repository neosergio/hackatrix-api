from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from utils.pagination import StandardResultsSetPagination
from .models import EvaluationCommittee
from .serializers import EvaluationCommitteeSerializer


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
