from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_moderator


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsJury(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_jury


class IsFromHR(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_from_HR


class IsFromEvaluationCommittee(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_from_evaluation_committee
