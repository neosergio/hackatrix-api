from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from utils.pagination import StandardResultsSetPagination
from utils.send_push_notification import send_message_android, send_message_ios

from .models import Event, Registrant
from .serializers import EventSerializer, EventFeaturedNotificationSerializer
from .serializers import RegistrantSerializer, RegistrantIdentitySerializer
from users.models import UserDevice, User


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
    participants = []
    if len(participants) > 0:
        response.update({'is_participant': True})
    else:
        response.update({'is_participant': False})
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def event_featured(request):
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    serializer = EventSerializer(event)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
    users = User.objects.all()
    serializer = EventFeaturedNotificationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        message = serializer.validated_data['message']
        for user in users:
            user_devices = UserDevice.objects.filter(user=user)
            for user_device in user_devices:
                if user_device.operating_system == 'android':
                    send_message_android(user_device.code, message)
                elif user_device.operating_system == 'ios':
                    send_message_ios(user_device.code, message)
                else:
                    return ValidationError('SO sin identificar')

        return Response(status=status.HTTP_200_OK)


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


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def registrant_list(request):
    registrants = Registrant.objects.all()
    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(registrants, request)
        serializer = RegistrantSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        serializer = RegistrantSerializer(registrants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.AllowAny, ))
@renderer_classes((StaticHTMLRenderer,))
def registrant_qr_code(request, email):
    registrant = get_object_or_404(Registrant, email=email)
    qr_code_url = "{}?data={}".format(settings.QR_CODE_CREATE_API_URL, registrant.code)
    data = "<img src='{}'>".format(qr_code_url)
    return Response(data)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def registrant_identity_validation(request):
    """
    Validates registrant identity QR code
    """
    serializer = RegistrantIdentitySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        code_to_validate = serializer.validated_data['registrant_qr_code']
        registrant = get_object_or_404(Registrant, code=code_to_validate)
        serializer = RegistrantSerializer(registrant)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((permissions.IsAdminUser, ))
def registrant_send_qr_code(request):
    registrants_without_email = Registrant.objects.filter(is_email_sent=False)

    for registrant in registrants_without_email:
        subject = "[{}] Conserva tu código QR para el evento".format(registrant.event.title)
        context = {'qr_code_create_api_url': settings.QR_CODE_CREATE_API_URL,
                   'registrant_full_name': registrant.full_name,
                   'registrant_qr_code': registrant.code}
        html_message = render_to_string('mail_template.html', context)
        plain_message = strip_tags(html_message)
        from_email = "{} <{}>".format(registrant.event.title, settings.EMAIL_HOST_USER)
        to = registrant.email
        try:
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except Exception as e:
            raise ValidationError(e)
    return Response(status.HTTP_200_OK)
