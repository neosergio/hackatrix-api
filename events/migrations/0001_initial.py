# Generated by Django 2.1.7 on 2019-04-16 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.URLField()),
                ('dates', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('details', models.TextField()),
                ('register_link', models.URLField(blank=True, null=True)),
                ('sharing_text', models.CharField(blank=True, max_length=140, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_upcoming', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'events',
                'ordering': ['-is_upcoming'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.CharField(max_length=11)),
                ('longitude', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Registrant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('code', models.CharField(blank=True, max_length=6, null=True)),
                ('is_code_used', models.BooleanField(default=False)),
                ('is_email_sent', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.URLField()),
                ('datetime', models.DateTimeField()),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('details', models.TextField()),
                ('register_link', models.URLField(blank=True, null=True)),
                ('sharing_text', models.CharField(blank=True, max_length=140, null=True)),
                ('is_interaction_active', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_track', to='events.Event')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Location')),
            ],
            options={
                'verbose_name_plural': 'event tracks',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='TrackItemAgenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=8)),
                ('text', models.CharField(max_length=255)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_item', to='events.Track')),
            ],
            options={
                'verbose_name': 'Agenda item',
                'verbose_name_plural': 'Agenda items',
                'ordering': ['time'],
            },
        ),
    ]
