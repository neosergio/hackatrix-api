from django.contrib.auth import logout
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.renderers import StaticHTMLRenderer

from .models import User, UserDevice
from .serializers import UserAuthenticationSerializer, UserSerializer, UserEmailSerializer, UserLogoutSerializer
from .serializers import UserCreationSerializer, UserUpdatePasswordSerializer, UserUpdateProfileSerialier


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Authenticate user with provided credentials and register user device
        """
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        device_code = serializer.validated_data['device_code']
        device_os = serializer.validated_data['device_os']
        UserDevice.objects.get_or_create(user=user, operating_system=device_os, code=device_code)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "data": {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'is_validated': user.is_validated,
            }
        })


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, ))
def user_create(request):
    """
    Creates a user account using email and password
    """
    serializer = UserCreationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.create_user(email=email, password=password)
        user.generate_validation_code()

        subject = "[Hackatrix] Valide su usuario para la Hackatrix"

        draft_message = """
                Una cuenta en la aplicación Hackatrix ha sido creada con su email.
                    Confirme esta creación dando clic en el siguiente enlace: %s
                Si usted no creo ningún usuario, ignore este mensaje."""

        current_site = Site.objects.get_current()
        user_validation_api = reverse("users:user_validation", kwargs={'user_uuid': user.validation_code})
        validation_url = current_site.domain + user_validation_api
        message = draft_message % (validation_url)

        try:
            send_mail = EmailMessage(subject, message, to=[user.email])
            send_mail.send()
        except Exception as e:
            print(e)
            content = {'detail': 'Problemas con el envio de emails'}
            return Response(content, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def user_profile(request):
    """
    Returns user detail
    """
    if request.GET.get('id'):
        user = get_object_or_404(User, pk=request.GET.get('id'))
    else:
        user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((permissions.IsAuthenticated, ))
def user_profile_update(request):
    """
    Updates user profile
    """
    user = request.user
    serializer = UserUpdateProfileSerialier(data=request.data)
    if serializer.is_valid(raise_exception=True):
        full_name = serializer.validated_data['full_name']
        user.full_name = full_name
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def user_logout(request):
    """
    Logout current user
    """
    serializer = UserLogoutSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        code = serializer.validated_data['device_code']
        device = UserDevice.objects.filter(code=code)
        device.delete()
        logout(request)
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH', ])
@permission_classes((permissions.IsAuthenticated, ))
def user_password_update(request):
    """
    Updates user password
    """
    serializer = UserUpdatePasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        user = request.user
        if user.check_password(current_password):
            user.set_password(new_password)
            user.is_password_reset_required = False
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            raise ValidationError('Password actual incorrecto.')


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, ))
def user_password_recovery_request(request):
    """
    Request user password recovery
    """
    serializer = UserEmailSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        user.generate_reset_password_code()

        subject = "[Hackatrix] Password nuevo solicitado"
        draft_message = """
        Una solicitud de restablecimiento de password ha sido recibida.
            Su password temporal es: %s
            Confirme su solicitud dando clic en el siguiente enlace: %s
        Si usted no solicito ningún restablecimiento, ignore este correo."""

        current_site = Site.objects.get_current()
        user_reset_confirmation_api = reverse("users:user_password_recovery_request")
        reset_url = current_site.domain + user_reset_confirmation_api + user.reset_password_code
        message = draft_message % (user.temporary_password, reset_url)

        try:
            send_email = EmailMessage(subject, message, to=[user.email])
            send_email.send()
        except Exception as e:
            print(e)
            content = {'detail: Problemas con el envio de correo electronico'}
            return Response(content, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.AllowAny, ))
@renderer_classes((StaticHTMLRenderer,))
def user_password_recovery_request_confirmation(request, user_uuid):
    """
    Confirms password recovery action
    """
    if request.method == 'GET':
        user = get_object_or_404(User, reset_password_code=user_uuid)
        user.set_password(user.temporary_password)
        user.reset_password_code = None
        user.temporary_password = None
        user.is_password_reset_required = True
        user.save()
        data = "<h1>Solicitud de reestablecimiento de password confirmada.</h1>"
        return Response(data)


@api_view(['GET', ])
@permission_classes((permissions.AllowAny, ))
@renderer_classes((StaticHTMLRenderer,))
def user_validation(request, user_uuid):
    """
    Confirms user creation
    """
    user = get_object_or_404(User, validation_code=user_uuid)
    user.is_validated = True
    user.save()
    data = "<h1>Email validado, retorne a la aplicación.</h1>"
    return Response(data)
