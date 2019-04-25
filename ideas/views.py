from django.shortcuts import get_object_or_404
from constance import config
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Idea, IdeaTeamMember
from .serializers import IdeaSerializer, IdeaCreationSerializer
from events.models import Event
from users.functions import validate_user_qr_code
from users.models import User
from users.permissions import IsModerator
from users.serializers import UserIdentitySerializer
from utils.pagination import StandardResultsSetPagination


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def idea_add_team_member(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    serializer = UserIdentitySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        code_to_validate = serializer.validated_data['user_qr_code']
        user = get_object_or_404(User, pk=code_to_validate[10:])

        if validate_user_qr_code(code_to_validate, user):
            if len(IdeaTeamMember.objects.filter(idea=idea)) < idea.max_number_of_participants:
                try:
                    IdeaTeamMember.objects.create(idea=idea, member=user)
                except Exception as e:
                    raise ValidationError(e)
                serializer = IdeaSerializer(idea)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                raise ValidationError(config.TEAM_MAX_SIZE_MESSAGE)
        else:
            raise ValidationError("Invalid code.")


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def idea_creation(request):
    serializer = IdeaCreationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        event = Event.objects.filter(is_featured=True).first()
        try:
            idea = Idea.objects.create(title=title, description=description, written_by=request.user, event=event)
        except Exception as e:
            raise ValidationError(e)
        serializer = IdeaSerializer(idea)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    serializer = IdeaSerializer(idea)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def idea_list_complete(request):
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    ideas = Idea.objects.filter(event=event)
    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(ideas, request)
        serializer = IdeaSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def idea_list_validated(request):
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    ideas = Idea.objects.filter(event=event, is_valid=True)
    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(ideas, request)
        serializer = IdeaSerializer(results, many=True)
        return paginator.get_paginated_response(results, many=True)
    else:
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((IsModerator, ))
def idea_validation_switch(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    if idea.is_valid:
        idea.is_valid = False
    else:
        idea.is_valid = True
    idea.save()
    serializer = IdeaSerializer(idea)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
