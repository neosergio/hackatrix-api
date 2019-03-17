from rest_framework import serializers

from .views import Idea


class IdeaSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Idea
        fields = "__all__"
