from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Idea
from .serializers import IdeaSerializer, IdeaCreationSerializer
from events.models import Event
from events.permissions import IsParticipant


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, IsParticipant))
def idea_creation(request):
    serializer = IdeaCreationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        author = request.user
        event = Event.objects.filter(is_featured=True).first()
        idea = Idea.objects.create(title=title, description=description, author=author, event=event)
        serializer = IdeaSerializer(idea)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, IsParticipant))
def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    serializer = IdeaSerializer(idea)
    return Response(serializer.data, status=status.HTTP_200_OK)
