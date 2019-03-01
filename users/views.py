from django.contrib.auth import logout
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import StaticHTMLRenderer

from .models import User
from .serializers import UserAuthenticationSerializer, UserSerializer, UserEmailSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Authenticate user with provided credentials
        ---
        serializer: users.serializers.py.UserAuthenticationSerializer
        response_serializer: users.serializers.py.UserAuthenticationResponseSerializer
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "data": [{
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'is_validated': user.is_validated,
            }]
        })


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, ))
def user_create(request):
    """
    Creates a user account using email and password
    """
    serializer = UserAuthenticationSerializer(data=request.data)
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


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def user_logout(request):
    """
    Logout current user
    """
    logout(request)
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, ))
def user_password_recovery_request(request):
    """
    Request user password recovery
    """
    serializer = UserEmailSerializer(data=request.data)
    print(serializer)
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
def user_validation(request, user_uuid):
    """
    Confirms user creation
    """
    user = get_object_or_404(User, validation_code=user_uuid)
    user.is_validated = True
    user.save()
    data = "<h1>Email validado, retorne a la aplicación.</h1>"
    return Response(data)
