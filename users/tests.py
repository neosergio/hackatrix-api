from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User
from .models import UserDevice
from .serializers import UserAuthenticationSerializer
from .serializers import UserCreationSerializer
from .serializers import UserUpdatePasswordSerializer
from .serializers import UserUpdateProfileSerialier


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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registration_not_using_mobile_client(self):
        data = {"email": "tester@hackatrix.com",
                "password": "password"}

        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(self.creation_url, serializer.data)

        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserTestCase(APITestCase):

    authentication_url = ("/users/authenticate/")
    creation_url = reverse("users:user_create")

    def setUp(self):
        self.user = User.objects.create_user(email="mobile@hackatrix.com",
                                             password="password",
                                             is_staff=True)
        self.user_device = UserDevice.objects.create(user=self.user,
                                                     operating_system="unknown",
                                                     code="unknown")
        self.token = Token.objects.get(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    def test_authentication_mobile_user(self):
        data = {"username": "mobile@hackatrix.com",
                "password": "password",
                "device_code": "QWERTYASDFG",
                "device_os": "iOS"}

        serializer = UserAuthenticationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(self.authentication_url, serializer.validated_data)

        self.assertEqual(serializer.is_valid(raise_exception=True), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authentication_non_mobile_user(self):
        data = {"username": "mobile@hackatrix.com",
                "password": "password"}

        serializer = UserAuthenticationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(self.authentication_url, serializer.validated_data)

        self.assertEqual(serializer.is_valid(raise_exception=True), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list(self):
        list_url = reverse("users:user_list")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_active_summary(self):
        user_active_summary_url = reverse("users:users_active_summary")
        response = self.client.get(user_active_summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile(self):
        profile_url = reverse("users:user_profile")
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_update(self):
        profile_update_url = reverse("users:user_profile_update")
        data = {"full_name": "First Name Last Name",
                "is_active": True,
                "is_staff": True,
                "is_jury": True,
                "is_from_evaluation_committee": False}
        serializer = UserUpdateProfileSerialier(data=data)
        if serializer.is_valid():
            response = self.client.patch(profile_update_url, serializer.validated_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_user_password_update(self):
        password_update_url = reverse("users:user_password_update")
        data = {"current_password": "password",
                "new_password": "password"}
        serializer = UserUpdatePasswordSerializer(data=data)
        if serializer.is_valid():
            response = self.client.patch(password_update_url, serializer.validated_data)

        self.assertTrue(self.user.check_password(serializer.validated_data.get("current_password")))
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

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
                "password": "password",
                "full_name": "Tester Tester",
                "is_active": True}

        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(self.creation_url, serializer.data)

        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        logout_url = reverse("users:user_logout")
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
