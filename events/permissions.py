from rest_framework import permissions
from .models import Participant


class IsParticipant(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        else:
            participants = Participant.objects.filter(user=user)
            if len(participants) > 0:
                participant = True
            else:
                participant = False
            return request.user and participant
