from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id',
                  'email',
                  'is_staff',
                  'is_active',
                  'is_validated')


class UserAuthenticationSerializer(AuthTokenSerializer):
    device_code = serializers.CharField(max_length=100)
    device_os = serializers.CharField(max_length=100)


class UserAuthenticationResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField()


class UserCreationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class UserEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)


class UserLogoutSerializer(serializers.Serializer):
    device_code = serializers.CharField(max_length=100)


class UserUpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
