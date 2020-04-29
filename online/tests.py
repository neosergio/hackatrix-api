from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User


class EvaluationCommitteeTestCase(APITestCase):

    evaluation_committee_list_url = reverse("online:evaluation_committee_list")

    def setUp(self):
        self.user = User.objects.create_user(email="test@hackatrix.com",
                                             password="password",
                                             is_staff=True)
        self.token = Token.objects.get(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    def test_committee_list(self):
        response = self.client.get(self.evaluation_committee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
