import os
from ast import literal_eval
from constance import config
from datetime import datetime, timezone
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import StaticHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from urllib.request import Request, urlopen
from utils.pagination import StandardResultsSetPagination
from utils.send_push_notification import send_message_android, send_message_ios

from .models import Event, Registrant, Attendance, RegistrantAttendance, Team, TeamMember
from .serializers import EventSerializer, EventFeaturedNotificationSerializer
from .serializers import RegistrantSerializer, RegistrantIdentitySerializer, AttendaceSerializer
from .serializers import TeamSerializer, TeamUpdateSerializer
from assessments.models import TeamAssessment
from users.models import UserDevice, User
from users.permissions import IsModerator


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
@permission_classes((permissions.IsAuthenticatedOrReadOnly, ))
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
        if request.GET.get('data') and (request.GET.get('data') == 'true'):
            response = {"data": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((permissions.IsAdminUser, ))
def registrant_send_qr_code(request):
    """
    Sends QR code to registrants emails
    """
    registrants_without_email = Registrant.objects.filter(is_email_sent=False)[:config.BULK_EMAIL_QUOTE]

    for registrant in registrants_without_email:
        subject = "[{}] GUARDÁ TU CÓDIGO QR PARA INGRESAR A LA HACKATRIX".format(registrant.event.title)
        context = {'qr_code_create_api_url': settings.QR_CODE_CREATE_API_URL,
                   'registrant_event_title': registrant.event.title,
                   'registrant_full_name': registrant.full_name,
                   'registrant_qr_code': registrant.code,
                   'days_left_to_event': config.DAYS_LEFT_TO_EVENT}
        html_message = render_to_string('mail_template.html', context)
        plain_message = strip_tags(html_message)
        from_email = "{} <{}>".format(registrant.event.title, settings.EMAIL_HOST_USER)
        to = registrant.email
        try:
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            registrant.is_email_sent = True
            registrant.save()
        except Exception as e:
            raise ValidationError(e)
    return Response(status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((permissions.IsAdminUser, ))
def registrant_email_sent_flag_to_false(request):
    """
    Changes to false is_email_sent flag for entire registrant list.
    """
    registrants = Registrant.objects.all()
    for registrant in registrants:
        registrant.is_email_sent = False
        registrant.save()
    return Response(status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def event_attendance_list(request):
    event = Event.objects.filter(is_active=True, is_featured=True).first()

    attendances = Attendance.objects.filter(event=event, is_active=True)
    attendances = attendances.filter(available_from__lte=datetime.now(timezone.utc),
                                     due_date__gte=datetime.now(timezone.utc))

    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(attendances, request)
        serializer = AttendaceSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        serializer = AttendaceSerializer(attendances, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def event_attendance_register(request, attendance_id):
    attendance = get_object_or_404(Attendance, pk=attendance_id)

    attendance_counter = len(RegistrantAttendance.objects.filter(attendance=attendance))
    if attendance.max_capacity is not None:
        if attendance_counter >= attendance.max_capacity:
            raise ValidationError('Capacidad máxima alcanzada')

    current_user = request.user
    serializer = RegistrantIdentitySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        registrant_qr_code = serializer.validated_data['registrant_qr_code']
        registrant = get_object_or_404(Registrant, code=registrant_qr_code)
        try:
            RegistrantAttendance.objects.create(
                registrant=registrant,
                attendance=attendance,
                registered_by=current_user)
        except Exception as e:
            raise ValidationError("Participante ya registrado - {}".format(e))
        attendance_counter = len(RegistrantAttendance.objects.filter(attendance=attendance))
        response = {'registrant_name': registrant.full_name,
                    'max_capacity': attendance.max_capacity,
                    'counter': attendance_counter}
        return Response(response, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def team_detail(request, team_id):
    response = dict()
    team = get_object_or_404(Team, pk=team_id)
    serializer = TeamSerializer(team)
    response.update(serializer.data)

    has_been_assessed = False
    team_assessment = TeamAssessment.objects.filter(team=team, evaluator=request.user).first()
    if team_assessment:
        has_been_assessed = team_assessment.has_been_assessed
    response.update({"has_been_assessed": has_been_assessed})

    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def team_list_event_featured(request):
    teams_response = list()
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    teams = Team.objects.filter(is_active=True, event=event, is_valid=True)

    for team in teams:
        team_assessment = TeamAssessment.objects.filter(team=team, evaluator=request.user).first()
        if team_assessment:
            has_been_assessed = team_assessment.has_been_assessed
        else:
            has_been_assessed = False
        teams_response.append({'id': team.id,
                               'title': team.title,
                               'event': team.event.id,
                               'description': team.description,
                               'table': team.table,
                               'help_to': team.help_to,
                               'is_active': team.is_active,
                               'is_valid': team.is_valid,
                               'has_been_assessed': has_been_assessed})

    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(teams_response, request)
        return paginator.get_paginated_response(results)
    else:
        return Response(teams_response, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((IsModerator, ))
def team_update(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    serializer = TeamUpdateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        team.title = serializer.validated_data['title']
        team.description = serializer.validated_data['description']
        team.table = serializer.validated_data['table']
        team.save()
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH', ])
@permission_classes((IsModerator, ))
def team_deactivate(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.is_active = False
    team.save()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((IsModerator, ))
@renderer_classes((JSONRenderer,))
def team_data_from_surveymonkey(request):
    request_data = Request(os.environ.get("SURVEY_MONKEY_URL") or "no-url")
    request_data.add_header('Authorization',
                            os.environ.get("AUTHORIZATION_SURVEYMONKEY_KEY") or "no-authorization-key")
    raw_content = urlopen(request_data).read()
    content = literal_eval(raw_content.decode('utf-8'))
    event = Event.objects.filter(is_active=True, is_featured=True).first()

    for item in content['data']:

        try:
            team_raw_data = item['pages'][0]['questions']
            table = team_raw_data[0]['answers'][0]['text']
            title = team_raw_data[1]['answers'][0]['text']
            description = team_raw_data[3]['answers'][0]['text']
        except Exception as e:
            print(e)
            pass

        try:
            team = Team.objects.create(title=title, event=event, description=description, table=table)
            participants = team_raw_data[2]['answers']
            for participant in participants:
                participant_name = participant['text']
                try:
                    TeamMember.objects.create(full_name=participant_name, team=team)
                except Exception as e:
                    print(e)
                    pass
        except Exception as e:
            print(e)
            pass

    return Response({'message': 'successfull'}, status=status.HTTP_200_OK)
