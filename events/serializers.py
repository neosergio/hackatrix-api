from rest_framework import serializers

from .models import Event, Track, Participant


class TrackSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Track
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    event_track = TrackSerializer(many=True)

    class Meta(object):
        model = Event
        fields = "__all__"


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Participant
        fields = "__all__"
