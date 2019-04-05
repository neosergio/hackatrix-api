from rest_framework import serializers

from .models import Idea, IdeaTeamMember
from users.serializers import UserSerializer


class IdeaTeamMember(serializers.ModelSerializer):
    member = UserSerializer()

    class Meta(object):
        model = IdeaTeamMember
        fields = "__all__"


class IdeaSerializer(serializers.ModelSerializer):
    idea_team_member = IdeaTeamMember(many=True)

    class Meta(object):
        model = Idea
        fields = "__all__"


class IdeaCreationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
