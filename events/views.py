from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from utils.pagination import StandardResultsSetPagination

from .models import Event
from .serializers import EventSerializer


@api_view(['GET', ])
@permission_classes((permissions.AllowAny, ))
def event_featured_list(request):
    """
    Returns event featured list
    """
    events = Event.objects.filter(is_active=True, is_featured=True)
    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
