from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from utils.pagination import StandardResultsSetPagination
from utils.send_push_notification import send_message_android, send_message_ios

from .models import Event, Participant, Registrant
from .serializers import EventSerializer, ParticipantSerializer, EventFeaturedNotificationSerializer
from users.models import UserDevice


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
@permission_classes((permissions.IsAuthenticated, ))
def event_featured(request):
    response = dict()
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    serializer = EventSerializer(event)
    response.update(serializer.data)
    participants = Participant.objects.filter(event=event, user=request.user)
    if len(participants) > 0:
        response.update({'is_participant': True})
    else:
        response.update({'is_participant': False})
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
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
@permission_classes((permissions.IsAdminUser, ))
def event_featured_send_notification(request):
    """
    Send notification to participants at event featured.
    """
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    participants = Participant.objects.filter(event=event)
    serializer = EventFeaturedNotificationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        message = serializer.validated_data['message']
        for participant in participants:
            user_devices = UserDevice.objects.filter(user=participant.user)
            for user_device in user_devices:
                if user_device.operating_system == 'android':
                    status_code = send_message_android(user_device.code, message)
                elif user_device.operating_system == 'ios':
                    status_code = send_message_ios(user_device.code, message)
                else:
                    return ValidationError('SO sin identificar')

                if int(status_code) < 200 or int(status_code) > 300:
                    UserDevice.objects.get(code=user_device.code).delete()

        return Response(status=status.HTTP_200_OK)


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
        participant.code_used = registrant.code
        participant.save()
        registrant.is_code_used = True
        registrant.save()
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((permissions.IsAdminUser, ))
def event_send_participant_codes(request):
    """
    Send email with participant code to registrants
    """
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    if request.GET.get('all') and (request.GET.get('all') == "true"):
        registrants = Registrant.objects.filter(event=event)
    else:
        registrants = Registrant.objects.filter(event=event, is_email_sent=False)

    subject = "[%s] Su código de participante" % (event.title)

    draft_message = """
                            Puede registrarse en la aplicación usando el codigo: %s.
                            Si usted no se registró, ignore este mensaje."""

    for registrant in registrants:
        message = draft_message % (registrant.code)
        send_mail = EmailMessage(subject, message, to=[registrant.email])

        try:
            send_mail.send()
            registrant.is_email_sent = True
            registrant.save()
        except Exception as e:
            raise ValidationError(e)

    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE', ])
@permission_classes((permissions.IsAdminUser, ))
def event_featured_reset_participants(request):
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    participants = Participant.objects.filter(event=event)

    for participant in participants:
        participant.delete()

    return Response(status.HTTP_202_ACCEPTED)
