from rest_framework import serializers

from .models import Assessment, FinalResult


class AssessmentSerializer(serializers.ModelSerializer):

    class Meta():
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


class FinalResultSerializer(serializers.ModelSerializer):

    class Meta():
        depth = 1
        model = FinalResult
        fields = "__all__"
