# Generated by Django 2.2.10 on 2020-04-29 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0002_auto_20200429_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='last_save',
            field=models.DateTimeField(auto_now=True),
        ),
    ]