# Generated by Django 2.2.10 on 2020-05-09 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0007_auto_20200507_0423'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='evaluation',
            unique_together={('user', 'team')},
        ),
    ]
