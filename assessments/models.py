from django.db import models


class Assessment(models.Model):
    title = models.CharField(max_length=50)
    weight = models.PositiveIntegerField(default=1)
    is_for_jury = models.BooleanField(default=False)
    is_for_evaluation_committee = models.BooleanField(default=False)
    is_for_HR = models.BooleanField(default=False)
    is_for_team_leader = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ProjectAssessment(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    idea = models.ForeignKey('ideas.Idea', on_delete=models.CASCADE)
    evaluator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    value = models.PositiveIntegerField(default=0)

    class Meta(object):
        unique_together = ('assessment', 'idea', 'evaluator')


class RegistrantAssessment(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    registrant = models.ForeignKey('events.Registrant', on_delete=models.CASCADE)
    evaluator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    value = models.PositiveIntegerField(default=0)

    class Meta(object):
        unique_together = ('assessment', 'registrant', 'evaluator')


class RegistrantComment(models.Model):
    comment = models.CharField(max_length=255)
    comment_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    registrant = models.ForeignKey('events.Registrant', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        unique_together = ('registrant', 'comment_by')


class TeamAssessment(models.Model):
    team = models.ForeignKey('events.Team', on_delete=models.CASCADE)
    evaluator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    has_been_assessed = models.BooleanField(default=False)


class TeamAssessmentResults(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    team = models.ForeignKey('events.Team', on_delete=models.CASCADE)
    evaluator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.value = self.value * self.assessment.weight
        super().save(*args, **kwargs)

    class Meta(object):
        ordering = ['-pk']
        unique_together = ['assessment', 'team', 'evaluator']
        verbose_name_plural = 'team assessment results'


class FinalResult(models.Model):
    team = models.ForeignKey('events.Team', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0, null=True, blank=True)
    type = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if self.score is None:
            self.score = 0
        super().save(*args, **kwargs)

    class Meta(object):
        ordering = ["-score"]
