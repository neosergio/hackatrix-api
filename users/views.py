from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import StaticHTMLRenderer

from .models import User
from .serializers import UserAuthenticationSerializer, UserSerializer


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
    Create user
    """
    serializer = UserAuthenticationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.create_user(email=email, password=password)
        user.generate_validation_code()
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
