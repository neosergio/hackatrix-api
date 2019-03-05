from django.db import models


class Idea(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    author = models.ForeignKey('users.User', related_name='author_idea', on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', related_name='event_idea', on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)

    class Meta(object):
        ordering = ['title']


class IdeaParticipant(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    participant = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta(object):
        ordering = ['idea']
        unique_together = ('idea', 'participant')
        verbose_name = 'Idea Participant'
        verbose_name_plural = 'Idea Participants'
