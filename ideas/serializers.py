from rest_framework import serializers

from .views import Idea


class IdeaSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Idea
        fields = "__all__"


class IdeaCreationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
