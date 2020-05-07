# Generated by Django 2.2.10 on 2020-05-07 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0004_auto_20200430_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='total_score',
            new_name='committee_score',
        ),
        migrations.AddField(
            model_name='team',
            name='jury_score',
            field=models.FloatField(default=0),
        ),
    ]