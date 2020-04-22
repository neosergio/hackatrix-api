from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User
from .models import UserDevice
from .serializers import UserAuthenticationSerializer
from .serializers import UserCreationSerializer


class RegistrationTestCase(APITestCase):

    creation_url = reverse("users:user_create")

    def test_registration_using_mobile_client(self):
        data = {"email": "tester@hackatrix.com",
                "password": "password",
                "device_code": "QWERTYASDFG",
                "device_os": "iOS"}

        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(self.creation_url, serializer.data)

        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_not_using_mobile_client(self):
        data = {"email": "tester@hackatrix.com",
                "password": "password"}

        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(self.creation_url, serializer.data)

        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTestCase(APITestCase):

    authentication_url = ("/users/authenticate/")

    def setUp(self):
        self.user = User.objects.create_user(email="mobile@hackatrix.com",
                                             password="password")
        self.user_device = UserDevice.objects.create(user=self.user,
                                                     operating_system="unknown",
                                                     code="unknown")
        self.token = Token.objects.get_or_create(user=self.user)

    def test_authentication_mobile_user(self):
        data = {"username": "mobile@hackatrix.com",
                "password": "password",
                "device_code": "QWERTYASDFG",
                "device_os": "iOS"}

        serializer = UserAuthenticationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(self.authentication_url, serializer.data)

        self.assertEqual(serializer.is_valid(raise_exception=True), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authentication_non_mobile_user(self):
        data = {"username": "mobile@hackatrix.com",
                "password": "password"}

        serializer = UserAuthenticationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(self.authentication_url, serializer.data)

        self.assertEqual(serializer.is_valid(raise_exception=True), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
