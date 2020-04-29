from rest_framework import serializers
from .models import EvaluationCommittee


class EvaluationCommitteeSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = EvaluationCommittee
        fields = "__all__"
