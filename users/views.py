from django.contrib.auth import logout
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


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
            }]
        })


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def user_logout(request):
    """
    Logout current user
    """
    logout(request)
    return Response(status=status.HTTP_202_ACCEPTED)
