from rest_framework import permissions
from .models import Participant


class IsParticipant(permissions.BasePermission):

    def has_permission(self, request, view):
        participants = Participant.objects.filter(user=request.user)
        if len(participants) > 0:
            participant = True
        else:
            participant = False
        return request.user and participant
