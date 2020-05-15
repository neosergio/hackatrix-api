from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id',
                  'email',
                  'full_name',
                  'is_active',
                  'is_staff',
                  'is_jury',
                  'is_from_evaluation_committee')


class UserAuthenticationSerializer(AuthTokenSerializer):
    device_code = serializers.CharField(max_length=200, required=False)
    device_os = serializers.CharField(max_length=10, required=False)


class UserAuthenticationResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField()


class UserCreationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    full_name = serializers.CharField(max_length=200, required=False)
    is_active = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)
    is_jury = serializers.BooleanField(default=False)
    is_from_evaluation_committee = serializers.BooleanField(default=False)
    device_code = serializers.CharField(max_length=200, required=False)
    device_os = serializers.CharField(max_length=10, required=False)


class UserIdentitySerializer(serializers.Serializer):
    user_qr_code = serializers.CharField(max_length=20)


class UserEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)


class UserLogoutSerializer(serializers.Serializer):
    device_code = serializers.CharField(max_length=200, required=False)


class UserUpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)


class UserUpdateProfileSerialier(serializers.Serializer):
    full_name = serializers.CharField(max_length=60)
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_jury = serializers.BooleanField()
    is_from_evaluation_committee = serializers.BooleanField()
