from rest_framework import serializers

from .models import Idea, IdeaTeamMember
from events.serializers import RegistrantSerializer


class IdeaTeamMember(serializers.ModelSerializer):
    member = RegistrantSerializer()

    class Meta(object):
        model = IdeaTeamMember
        fields = "__all__"


class IdeaSerializer(serializers.ModelSerializer):
    author = RegistrantSerializer()
    idea_team_member = RegistrantSerializer(many=True)

    class Meta(object):
        model = Idea
        fields = "__all__"


class IdeaCreationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    author_id = serializers.CharField()
