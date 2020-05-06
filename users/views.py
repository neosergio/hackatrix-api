from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import renderer_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response

from utils.pagination import StandardResultsSetPagination
from .functions import generate_user_qr_code
from .functions import validate_user_email
from .functions import validate_user_qr_code
from .models import User
from .models import UserDevice
from .serializers import UserAuthenticationSerializer
from .serializers import UserCreationSerializer
from .serializers import UserEmailSerializer
from .serializers import UserIdentitySerializer
from .serializers import UserLogoutSerializer
from .serializers import UserSerializer
from .serializers import UserUpdatePasswordSerializer
from .serializers import UserUpdateProfileSerialier


# from events.models import Registrant


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Authenticate user with provided credentials and register user device
        """
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')

        try:
            device_code = serializer.validated_data['device_code']
            device_os = serializer.validated_data['device_os']
        except Exception as e:
            print(e)
            device_code = device_os = "unknown"
        UserDevice.objects.get_or_create(user=user, operating_system=device_os, code=device_code)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "data": {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'full_name': user.full_name,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'is_jury': user.is_jury,
                'is_from_evaluation_committee': user.is_from_evaluation_committee,
                'is_blocked': user.is_blocked
            }
        })


@api_view(['POST', ])
@permission_classes((permissions.IsAdminUser, ))
def user_create(request):
    """
    Creates a user account using email and password
    """
    serializer = UserCreationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data.get('email')
        # registrant_emails = Registrant.objects.filter(email=email)
        # if len(registrant_emails) > 0:
        #    raise PermissionDenied('El email esta registrado como participante, no puede ser usuario')

        password = serializer.validated_data.get('password')
        full_name = serializer.validated_data.get('full_name')
        is_active = serializer.validated_data.get('is_active')
        is_staff = serializer.validated_data.get('is_staff')
        is_jury = serializer.validated_data.get('is_jury')
        is_from_evaluation_committee = serializer.validated_data.get('is_from_evaluation_committee')
        try:
            validate_password(password)
            if validate_user_email(email):
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    full_name=full_name,
                    is_active=is_active,
                    is_staff=is_staff,
                    is_jury=is_jury,
                    is_from_evaluation_committee=is_from_evaluation_committee)
                user.generate_validation_code()

                try:
                    device_code = serializer.validated_data['device_code']
                    device_os = serializer.validated_data['device_os']
                except Exception as e:
                    print(e)
                    device_code = device_os = 'unknown'
                UserDevice.objects.get_or_create(user=user, operating_system=device_os, code=device_code)

                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "data": {
                        'token': token.key,
                        'user_id': user.pk,
                        'email': user.email,
                        'is_active': user.is_active
                    }
                })
            else:
                raise PermissionDenied('Invalid email.')
        except Exception as e:
            raise ValidationError(e)


@api_view(['GET', ])
@permission_classes((permissions.IsAdminUser, ))
def user_list(request):
    """
    Returns user list
    """
    users = User.objects.all()

    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        serializer = UserSerializer(users, many=True)
        response = {
            'data': {'users': serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def user_identity(request):
    """
    Returns one time use code to generate QR
    """
    user = request.user
    return Response({'user_qr_code': generate_user_qr_code(user)}, status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def user_identity_validation(request):
    """
    Validates user identity code
    """
    serializer = UserIdentitySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        code_to_validate = serializer.validated_data.get('user_qr_code')
        user = get_object_or_404(User, pk=code_to_validate[10:])
        serializer = UserSerializer(user)

        if validate_user_qr_code(code_to_validate, user):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Invalid code.")


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
    response = {"data": serializer.data}
    return Response(response, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((permissions.IsAuthenticated, ))
def user_profile_update(request):
    """
    Updates user profile
    """
    if request.GET.get('id'):
        user = get_object_or_404(User, pk=request.GET.get('id'))
    else:
        user = request.user

    serializer = UserUpdateProfileSerialier(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user.full_name = serializer.validated_data.get('full_name')
        user.is_active = serializer.validated_data.get('is_active')
        user.is_staff = serializer.validated_data.get('is_staff')
        user.is_jury = serializer.validated_data.get('is_jury')
        user.is_from_evaluation_committee = serializer.validated_data.get('is_from_evaluation_committee')
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
        try:
            code = serializer.validated_data['device_code']
            device = UserDevice.objects.filter(code=code)
        except Exception:
            device = UserDevice.objects.filter(user=request.user)
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
        current_password = serializer.validated_data.get('current_password')
        new_password = serializer.validated_data.get('new_password')
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
        email = serializer.validated_data.get('email')
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


@api_view(['GET', ])
@permission_classes((permissions.IsAdminUser, ))
def users_active_summary(request):
    """
    Returns user active data summary: active users and total users
    """
    users = User.objects.all()
    active_users = users.filter(is_active=True)
    data = {"active_users": len(active_users),
            "total": len(users)}
    response = {"data": data}
    return Response(response, status=status.HTTP_200_OK)
