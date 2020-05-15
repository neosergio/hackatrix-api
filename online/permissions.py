from rest_framework import permissions

from .models import Evaluator


class IsEvaluator(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        evaluator = Evaluator.objects.filter(user=user)
        evaluator_flag = False
        if len(evaluator) > 0:
            evaluator_flag = True
        return request.user and evaluator_flag
