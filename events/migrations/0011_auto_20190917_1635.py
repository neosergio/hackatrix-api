# Generated by Django 2.1.7 on 2019-09-17 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20190912_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='table',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together={('title', 'description')},
        ),
    ]
