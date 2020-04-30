from rest_framework import serializers

from users.models import User
from .models import EvaluationCommittee
from .models import Evaluator


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
        fields = ('id', 'name', 'is_evaluation_closed', 'is_active', 'evaluator_committee')
