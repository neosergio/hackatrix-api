# Generated by Django 2.1.7 on 2019-09-10 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_team_teammember'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_evaluated', models.BooleanField(default=False)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Team')),
            ],
        ),
    ]
