from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Idea
from .serializers import IdeaSerializer
from events.permissions import IsParticipant


@api_view(('GET',))
@permission_classes((permissions.IsAuthenticated, IsParticipant))
def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    serializer = IdeaSerializer(idea)
    return Response(serializer.data, status=status.HTTP_200_OK)
