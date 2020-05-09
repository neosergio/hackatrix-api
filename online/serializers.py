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


class EvaluatorSerializer(serializers.ModelSerializer):
    user = UserEvaluatorSerializer()

    class Meta(object):
        model = Evaluator
        fields = ('user', 'is_active')


class EvaluationCommitteeSerializer(serializers.ModelSerializer):
    evaluator_committee = EvaluatorSerializer(many=True)

    class Meta(object):
        model = EvaluationCommittee
        fields = ('id', 'name', 'is_active', 'evaluator_committee')


class TeamSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Team
        fields = "__all__"


class TeamMemberCreationSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    email = serializers.EmailField()
    team = serializers.IntegerField()


class TeamMemberSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = TeamMember
        fields = "__all__"
