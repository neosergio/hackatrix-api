from rest_framework import serializers

from .models import Event, Track, TrackItemAgenda, Location, Registrant, Attendance, Team, TeamMember


class LocationSerializer(serializers.ModelSerializer):

    class Meta():
        model = Location
        fields = "__all__"


class TrackItemAgendaSerializer(serializers.ModelSerializer):

    class Meta():
        model = TrackItemAgenda
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    track_item = TrackItemAgendaSerializer(many=True)

    class Meta():
        model = Track
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    event_track = TrackSerializer(many=True)

    class Meta():
        model = Event
        fields = ('id', 'title', 'image', 'dates', 'address', 'register_link', 'is_featured', 'event_track')


class EventFeaturedNotificationSerializer(serializers.Serializer):
    message = serializers.CharField()


class RegistrantSerializer(serializers.ModelSerializer):

    class Meta():
        model = Registrant
        fields = "__all__"


class RegistrantIdentitySerializer(serializers.Serializer):
    registrant_qr_code = serializers.CharField(max_length=20)


class AttendaceSerializer(serializers.ModelSerializer):

    class Meta():
        model = Attendance
        fields = "__all__"


class TeamMemberSerializer(serializers.ModelSerializer):

    class Meta():
        model = TeamMember
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    team_member = TeamMemberSerializer(many=True)

    class Meta():
        model = Team
        fields = "__all__"


class TeamUpdateSerializer(serializers.Serializer):
    title = serializers.CharField()
    summary = serializers.CharField()
    description = serializers.CharField()
    table = serializers.CharField()
