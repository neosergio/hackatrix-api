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


class RegistrantAssessment(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    registrant = models.ForeignKey('events.Registrant', on_delete=models.CASCADE)
    evaluator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class RegistrantComment(models.Model):
    comment = models.CharField(max_length=255)
    comment_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    registrant = models.ForeignKey('events.Registrant', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
