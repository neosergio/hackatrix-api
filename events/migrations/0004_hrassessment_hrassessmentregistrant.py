# Generated by Django 2.1.7 on 2019-05-05 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0003_auto_20190503_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='HRAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('icon', models.URLField()),
                ('description', models.CharField(blank=True, default=True, max_length=255)),
                ('weight', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='HRAssessmentRegistrant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(default=0)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('registrant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Registrant')),
            ],
        ),
    ]
