from django.shortcuts import get_object_or_404
from constance import config
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from .models import Idea, IdeaTeamMember
from .serializers import IdeaSerializer, IdeaCreationSerializer, IdeaTeamMemberBulkSerializer
from assessments.models import ProjectAssessment
from events.models import Event, Registrant
from events.serializers import RegistrantIdentitySerializer
from users.permissions import IsModerator
from utils.pagination import StandardResultsSetPagination


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def idea_creation(request):
    """
    Creates an idea
    """
    serializer = IdeaCreationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        author = get_object_or_404(Registrant, pk=serializer.validated_data['author_id'])
        event = Event.objects.filter(is_featured=True).first()
        is_valid = serializer.validated_data['is_valid']
        try:
            idea = Idea.objects.create(title=title,
                                       description=description,
                                       author=author,
                                       written_by=request.user,
                                       event=event,
                                       is_valid=is_valid)
        except Exception as e:
            raise ValidationError(e)
        serializer = IdeaSerializer(idea)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((permissions.IsAuthenticated, ))
def idea_add_team_member(request, idea_id):
    """
    Add team member to a project / idea.
    """
    idea = get_object_or_404(Idea, pk=idea_id, is_valid=True)
    serializer = RegistrantIdentitySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        code_to_validate = serializer.validated_data['registrant_qr_code']
        registrant = get_object_or_404(Registrant, code=code_to_validate)
        registrant_ideas = Idea.objects.filter(is_valid=True, author=registrant)
        if len(registrant_ideas) > 0:
            raise PermissionDenied("Participante es autor de una idea")

        if len(IdeaTeamMember.objects.filter(idea=idea)) < idea.max_number_of_participants:
            try:
                IdeaTeamMember.objects.create(idea=idea, member=registrant)
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
def idea_add_team_member_list(request, idea_id):
    """
    Add team members list to a project / idea
    """
    idea = get_object_or_404(Idea, pk=idea_id, is_valid=True)
    serializer = IdeaTeamMemberBulkSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        idea_team_members = serializer.validated_data['idea_team_members']
        for team_member in idea_team_members:
            registrant = get_object_or_404(Registrant, code=team_member['registrant_qr_code'])
            registrant_ideas = Idea.objects.filter(is_valid=True, author=registrant)
            if len(registrant_ideas) > 0:
                pass
            elif len(IdeaTeamMember.objects.filter(idea=idea)) < idea.max_number_of_participants:
                try:
                    IdeaTeamMember.objects.create(idea=idea, member=registrant)
                except Exception as e:
                    raise ValidationError(e)
            else:
                raise ValidationError(config.TEAM_MAX_SIZE_MESSAGE)
        serializer = IdeaSerializer(idea)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        raise ValidationError("Invalid codes.")


@api_view(['DELETE', ])
@permission_classes((IsModerator, ))
def idea_remove_team_member(request, idea_id):
    """
    Removes team member from a project/idea
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    serializer = RegistrantIdentitySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        code_to_validate = serializer.validated_data['registrant_qr_code']
        registrant = get_object_or_404(Registrant, code=code_to_validate)
        IdeaTeamMember.objects.get(idea=idea, member=registrant).delete()
        serializer = IdeaSerializer(idea)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['DELETE', ])
@permission_classes((IsModerator, ))
def idea_remove_team_member_list(request, idea_id):
    """
    Removes team members list to a project / idea
    """
    idea = get_object_or_404(Idea, pk=idea_id, is_valid=True)
    serializer = IdeaTeamMemberBulkSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        idea_team_members = serializer.validated_data['idea_team_members']
        for team_member in idea_team_members:
            try:
                registrant = get_object_or_404(Registrant, code=team_member['registrant_qr_code'])
                IdeaTeamMember.objects.get(idea=idea, member=registrant).delete()
            except Exception as e:
                print(e)
                pass
        serializer = IdeaSerializer(idea)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        raise ValidationError("Invalid codes.")


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def idea_detail(request, idea_id):
    """
    Returns an idea detail
    """
    response = dict()
    idea = get_object_or_404(Idea, pk=idea_id)
    serializer = IdeaSerializer(idea)
    response.update(serializer.data)
    user = request.user
    assessments = ProjectAssessment.objects.filter(evaluator=user, idea=idea)
    if len(assessments) > 0:
        response.update({'has_been_assessed': True})
    else:
        response.update({'has_been_assessed': False})
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def idea_list_complete(request):
    """
    Returns full idea list
    """
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    ideas = Idea.objects.filter(event=event, is_active=True)
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
    """
    Returns full idea validated list
    """
    event = Event.objects.filter(is_active=True, is_featured=True).first()
    ideas = Idea.objects.filter(event=event, is_valid=True, is_active=True)
    if request.GET.get('page') or request.GET.get('per_page'):
        paginator = StandardResultsSetPagination()
        results = paginator.paginate_queryset(ideas, request)
        serializer = IdeaSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((IsModerator, ))
def idea_validation_switch(request, idea_id):
    """
    Switches idea is_valid flag between false or true
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    if idea.is_valid:
        idea.is_valid = False
    else:
        idea.is_valid = True
    idea.save()
    serializer = IdeaSerializer(idea)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated, ))
def author_idea_list(request, registrant_id):
    """
    Returns author ideas
    """
    registrant = get_object_or_404(Registrant, pk=registrant_id)
    ideas = Idea.objects.filter(author=registrant)
    serializer = IdeaSerializer(ideas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
