from rest_framework import serializers

from events.serializers import RegistrantIdentitySerializer
from events.serializers import RegistrantSerializer
from .models import Idea
from .models import IdeaTeamMember


class IdeaTeamMemberSerializer(serializers.ModelSerializer):
    member = RegistrantSerializer()

    class Meta():
        model = IdeaTeamMember
        fields = "__all__"


class IdeaSerializer(serializers.ModelSerializer):
    author = RegistrantSerializer()
    idea_team_member = IdeaTeamMemberSerializer(many=True)

    class Meta():
        model = Idea
        fields = "__all__"


class IdeaCreationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    is_valid = serializers.BooleanField()


class IdeaTeamMemberBulkSerializer(serializers.Serializer):
    idea_team_members = RegistrantIdentitySerializer(many=True)
