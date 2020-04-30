from django.db import models


class EvaluationCommittee(models.Model):
    name = models.CharField(max_length=100)
    is_evaluation_closed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Evaluator(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    evaluation_committee = models.ForeignKey(EvaluationCommittee,
                                             on_delete=models.CASCADE,
                                             related_name='evaluator_committee')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email


class Team(models.Model):
    name = models.CharField(max_length=100)
    project_description = models.TextField()
    project = models.CharField(max_length=100)
    total_score = models.FloatField(default=0)
    evaluation_committee = models.ForeignKey(EvaluationCommittee, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta(object):
        ordering = ['email']
        verbose_name = 'team member'
        verbose_name_plural = 'team members'


class Evaluation(models.Model):
    user = models.ForeignKey(Evaluator, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    total_score = models.FloatField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    last_save = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "f'{self.user.email} {str(self.total_score)}"


class CategoryScore(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.FloatField()
    is_committee_score = models.BooleanField(default=False)
    score = models.FloatField(default=0)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
