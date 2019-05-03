from rest_framework import serializers

from .models import Idea, IdeaTeamMember
from events.serializers import RegistrantSerializer, RegistrantIdentitySerializer


class IdeaTeamMemberSerializer(serializers.ModelSerializer):
    member = RegistrantSerializer()

    class Meta(object):
        model = IdeaTeamMember
        fields = "__all__"


class IdeaSerializer(serializers.ModelSerializer):
    author = RegistrantSerializer()
    idea_team_member = IdeaTeamMemberSerializer(many=True)

    class Meta(object):
        model = Idea
        fields = "__all__"


class IdeaCreationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    author_id = serializers.CharField()
    is_valid = serializers.BooleanField()


class IdeaTeamMemberBulkSerializer(serializers.Serializer):
    idea_team_members = RegistrantIdentitySerializer(many=True)
