# Generated by Django 2.2.10 on 2020-02-23 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_registrant_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrant',
            name='is_participant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registrant',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registrant',
            name='is_supplier',
            field=models.BooleanField(default=False),
        ),
    ]