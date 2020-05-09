from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User
from .models import Team
from .serializers import TeamMemberCreationSerializer


class EvaluationCommitteeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@hackatrix.com",
                                             password="password",
                                             is_staff=True)
        self.token = Token.objects.get(user=self.user)
        self.team = Team.objects.create(name="Team", project="Project", project_description="Description")
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    def test_committee_list(self):
        evaluation_committee_list_url = reverse("online:evaluation_committee_list")
        response = self.client.get(evaluation_committee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_detail(self):
        team_detail_url = reverse("online:team_detail", args=[self.team.pk])
        response = self.client.get(team_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_list(self):
        team_list_url = reverse("online:team_list")
        response = self.client.get(team_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_member_creation(self):
        team_member_creation_url = reverse("online:team_member_creation")
        data = {"name": "Name",
                "surname": "Surname",
                "email": "name@email.com",
                "team": self.team.pk}
        serializer = TeamMemberCreationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(team_member_creation_url, serializer.data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
