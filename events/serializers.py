from rest_framework import serializers

from .models import Event, Track, Participant, Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Location
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta(object):
        model = Track
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    event_track = TrackSerializer(many=True)

    class Meta(object):
        model = Event
        fields = ('id', 'title', 'image', 'dates', 'address', 'register_link', 'is_featured', 'event_track')


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Participant
        fields = "__all__"
