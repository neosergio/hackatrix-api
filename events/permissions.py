from rest_framework import permissions


class IsParticipant(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        else:
            participants = []
            if len(participants) > 0:
                participant = True
            else:
                participant = False
            return request.user and participant
