from itertools import chain
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Assessment
from .serializers import AssessmentSerializer
from users.permissions import IsProjectEvaluator


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
