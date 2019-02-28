from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id',
                  'email',
                  'is_staff',
                  'is_active',
                  'is_validated')


class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class UserAuthenticationResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField()
