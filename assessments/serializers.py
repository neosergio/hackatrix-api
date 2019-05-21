from rest_framework import serializers

from .models import Assessment


class AssessmentSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Assessment
        fields = '__all__'


class ScoreSerializer(serializers.Serializer):
    assessment_id = serializers.IntegerField()
    value = serializers.IntegerField()


class AssessmentResultSerializer(serializers.Serializer):
    assessment = AssessmentSerializer()
    value = serializers.IntegerField()


class ScoreBulkSerializer(serializers.Serializer):
    score_list = ScoreSerializer(many=True)
