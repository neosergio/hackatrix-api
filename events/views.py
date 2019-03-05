from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from utils.pagination import StandardResultsSetPagination

from .models import Event, Participant, Registrant
from .serializers import EventSerializer, ParticipantSerializer


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def event_detail(request, event_id):
    """
    Returns event detail by user
    """
    response = dict()
    event = get_object_or_404(Event, pk=event_id)
    serializer = EventSerializer(event)
    response.update(serializer.data)
    participants = Participant.objects.filter(event=event, user=request.user)
    if len(participants) > 0:
        response.update({'is_participant': True})
    else:
        response.update({'is_participant': False})
    return Response(response, status=status.HTTP_200_OK)


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


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def event_register_participant(request, code):
    """
    Registers a user as a participant using a code
    """
    user = request.user
    registrant = get_object_or_404(Registrant, code=code)

    if registrant.is_code_used:
        raise ValidationError("El código ya fue usado.")
    else:
        participant = Participant.objects.create(event=registrant.event, user=user)
        registrant.is_code_used = True
        registrant.save()
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
