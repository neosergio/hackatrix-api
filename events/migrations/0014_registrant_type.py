# Generated by Django 3.0.3 on 2020-02-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20190918_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrant',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]