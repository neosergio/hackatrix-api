# Generated by Django 2.2.10 on 2020-05-14 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0009_auto_20200513_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='evaluation_committee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_committee', to='online.EvaluationCommittee'),
        ),
    ]
