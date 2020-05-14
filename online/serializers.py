from rest_framework import serializers

from users.models import User
from .models import EvaluationCommittee
from .models import Evaluator
from .models import Team
from .models import TeamMember


class UserEvaluatorSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id', 'email')


class TeamSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Team
        fields = "__all__"


class EvaluatorSerializer(serializers.ModelSerializer):
    user = UserEvaluatorSerializer()

    class Meta(object):
        model = Evaluator
        fields = ('user', 'is_active')


class EvaluatorCommitteeSerializer(serializers.Serializer):
    committee_id = serializers.IntegerField()


class EvaluationCommitteeSerializer(serializers.ModelSerializer):
    evaluator_committee = EvaluatorSerializer(many=True)
    team_committee = TeamSerializer(many=True)

    class Meta(object):
        model = EvaluationCommittee
        fields = ('id', 'name', 'is_active', 'evaluator_committee', 'team_committee')


class ScoreSerializer(serializers.Serializer):
    name = serializers.CharField()
    percentage = serializers.FloatField()
    score = serializers.FloatField()


class EvaluationSaveSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    scores = ScoreSerializer(many=True)


class TeamCreationSerializer(serializers.Serializer):
    name = serializers.CharField()
    project = serializers.CharField()
    project_description = serializers.CharField()


class TeamMemberCreationSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    email = serializers.EmailField()
    team = serializers.IntegerField()


class TeamMemberSimpleSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    email = serializers.EmailField()


class TeamMemberSaveSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    members = TeamMemberSimpleSerializer(many=True)


class TeamMemberSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = TeamMember
        fields = "__all__"


class TeamUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    project = serializers.CharField()
    project_description = serializers.CharField()
