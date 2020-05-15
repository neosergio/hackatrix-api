from rest_framework import permissions

from .models import Evaluator


class IsEvaluator(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        else:
            evaluator = Evaluator.objects.filter(user=user)
            if len(evaluator) > 0:
                evaluator_flag = True
            else:
                evaluator_flag = False

            return request.user and evaluator_flag
