from django.db import models


class Idea(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    author = models.ForeignKey('events.Registrant',
                               related_name='author_idea',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)
    written_by = models.ForeignKey('users.User',
                                   related_name='written_idea',
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)
    event = models.ForeignKey('events.Event', related_name='event_idea', on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)
    max_number_of_participants = models.PositiveIntegerField(default=8)

    class Meta(object):
        ordering = ['title']

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


class JuryAssessments(models.Model):
    title = models.CharField(max_length=100)
    icon = models.URLField()
    description = models.CharField(max_length=255, blank=True, default=True)
    weight = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class JuryAssessmentIdea(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    jury = models.ForeignKey('users.User', on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)


class ModeratorAssesssment(models.Model):
    title = models.CharField(max_length=100)
    icon = models.URLField()
    description = models.CharField(max_length=255, blank=True, default=True)
    weight = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class ModeratorAssessmentIdea(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    moderator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)
