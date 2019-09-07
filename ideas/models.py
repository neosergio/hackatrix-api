from django.db import models


class Idea(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    author = models.OneToOneField('events.Registrant',
                                  related_name='author_idea',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)
    written_by = models.ForeignKey('users.User',
                                   related_name='written_idea',
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)
    event = models.ForeignKey('events.Event',
                              related_name='event_idea',
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    is_valid = models.BooleanField(default=False)
    max_number_of_participants = models.PositiveIntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta(object):
        ordering = ['-created_at', '-id']

    def __str__(self):
        return self.title


class IdeaTeamMember(models.Model):
    idea = models.ForeignKey(Idea, related_name='idea_team_member', on_delete=models.CASCADE)
    member = models.OneToOneField('events.Registrant', related_name='member_idea', on_delete=models.CASCADE)

    class Meta(object):
        ordering = ['idea']
        unique_together = ('idea', 'member')
        verbose_name = 'Team Member'
        verbose_name_plural = 'Groups'
