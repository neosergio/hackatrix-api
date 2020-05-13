from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User
from .models import Team, Evaluator, EvaluationCommittee
from .serializers import EvaluationSaveSerializer
from .serializers import TeamCreationSerializer
from .serializers import TeamMemberSaveSerializer
from .serializers import TeamMemberCreationSerializer
from .serializers import TeamUpdateSerializer


class EvaluationCommitteeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@hackatrix.com",
                                             password="password",
                                             is_staff=True,
                                             is_jury=True)
        self.token = Token.objects.get(user=self.user)
        self.team = Team.objects.create(name="Team", project="Project", project_description="Description")
        self.evaluation_committee = EvaluationCommittee.objects.create(name="Committee 01")
        self.evaluator = Evaluator.objects.create(user=self.user, evaluation_committee=self.evaluation_committee)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    def test_evaluation_save(self):
        evaluation_save_url = reverse("online:evaluation_save")
        data = {"team_id": self.team.pk,
                "scores": [{"name": "score 01",
                            "percentage": 10,
                            "score": 5
                            },
                           {"name": "score 02",
                            "percentage": 20,
                            "score": 10}]}
        serializer = EvaluationSaveSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(evaluation_save_url, serializer.data, format='json')

        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_committee_list(self):
        evaluation_committee_list_url = reverse("online:evaluation_committee_list")
        response = self.client.get(evaluation_committee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_creation(self):
        team_creation_url = reverse("online:team_creation")
        data = {"name": "Team 02",
                "project": "Project 02",
                "project_description": "Project Description 02"}
        serializer = TeamCreationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(team_creation_url, serializer.data, format='json')

        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_team_detail(self):
        team_detail_url = reverse("online:team_detail", args=[self.team.pk])
        response = self.client.get(team_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_list(self):
        team_list_url = reverse("online:team_list")
        response = self.client.get(team_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_member(self):
        team_member_url = reverse("online:team_member")
        data = {"team_id": self.team.pk,
                "members": [{"name": "Team member name 01",
                             "surname": "Team member surname 01",
                             "email": "teammember01@email.com"
                             },
                            {"name": "Team member name 01",
                             "surname": "Team member surname 02",
                             "email": "teammember02@email.com"}]}
        serializer = TeamMemberSaveSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(team_member_url, serializer.data, format='json')

        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_team_member_creation(self):
        team_member_creation_url = reverse("online:team_member_creation")
        data = {"name": "Name",
                "surname": "Surname",
                "email": "name@email.com",
                "team": self.team.pk}
        serializer = TeamMemberCreationSerializer(data=data)
        if serializer.is_valid():
            response = self.client.post(team_member_creation_url, serializer.data, format='json')

        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_team_list_to_evaluate(self):
        team_list_to_evaluate_url = reverse("online:team_list_to_evaluate")
        response = self.client.get(team_list_to_evaluate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_update(self):
        team_update_url = reverse("online:team_update")
        data = {"id": self.team.pk,
                "name": "Team 01.1",
                "project": "Project 01.1",
                "project_description": "Project Description 01.1"}
        serializer = TeamUpdateSerializer(data=data)
        if serializer.is_valid():
            response = self.client.patch(team_update_url, serializer.data, format='json')

        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_team_to_evaluate(self):
        team_to_evaluate_url = reverse("online:team_to_evaluate", args=[self.team.pk])
        response = self.client.get(team_to_evaluate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
