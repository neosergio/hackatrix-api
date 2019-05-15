from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id',
                  'email',
                  'full_name',
                  'is_staff',
                  'is_active',
                  'is_validated',
                  'is_jury',
                  'is_from_HR',
                  'is_from_evaluation_committee',
                  'is_moderator',
                  'is_blocked',
                  'is_password_reset_required')


class UserAuthenticationSerializer(AuthTokenSerializer):
    device_code = serializers.CharField(max_length=200)
    device_os = serializers.CharField(max_length=10)


class UserAuthenticationResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField()


class UserCreationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    device_code = serializers.CharField(max_length=200)
    device_os = serializers.CharField(max_length=10)


class UserIdentitySerializer(serializers.Serializer):
    user_qr_code = serializers.CharField(max_length=20)


class UserEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)


class UserLogoutSerializer(serializers.Serializer):
    device_code = serializers.CharField(max_length=200)


class UserUpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)


class UserUpdateProfileSerialier(serializers.Serializer):
    full_name = serializers.CharField(max_length=60)
