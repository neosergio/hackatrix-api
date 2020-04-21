from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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
