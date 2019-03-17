from django.db import models


class Idea(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    author = models.ForeignKey('users.User', related_name='author_idea', on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', related_name='event_idea', on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)
    max_number_of_participants = models.PositiveIntegerField(default=8)

    class Meta(object):
        ordering = ['title']


class IdeaTeamMember(models.Model):
    idea = models.ForeignKey(Idea, related_name='idea_team_member', on_delete=models.CASCADE)
    member = models.ForeignKey('users.User', related_name='member_idea', on_delete=models.CASCADE)

    class Meta(object):
        ordering = ['idea']
        unique_together = ('idea', 'member')
        verbose_name = 'Team Member'
        verbose_name_plural = 'Groups'
