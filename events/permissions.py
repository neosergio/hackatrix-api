from rest_framework import permissions


class IsParticipant(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        participants = []
        participant = False
        if len(participants) > 0:
            participant = True
        return request.user and participant
