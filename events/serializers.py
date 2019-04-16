from rest_framework import serializers

from .models import Event, Track, TrackItemAgenda, Location, Registrant


class LocationSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Location
        fields = "__all__"


class TrackItemAgenda(serializers.ModelSerializer):

    class Meta(object):
        model = TrackItemAgenda
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    track_item = TrackItemAgenda(many=True)

    class Meta(object):
        model = Track
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    event_track = TrackSerializer(many=True)

    class Meta(object):
        model = Event
        fields = ('id', 'title', 'image', 'dates', 'address', 'register_link', 'is_featured', 'event_track')


class EventFeaturedNotificationSerializer(serializers.Serializer):
    message = serializers.CharField()


class RegistrantSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Registrant
        fields = "__all__"
