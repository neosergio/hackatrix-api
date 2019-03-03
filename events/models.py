from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=11)
    longitude = models.CharField(max_length=11)

    def __str__(self):
        return "%s, %s, %s" % (self.name, self.latitude, self.longitude)


class Event(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField()
    dates = models.CharField(max_length=255)
    address = models.CharField(max_length=200, blank=True, null=True)
    details = models.TextField()
    register_link = models.URLField(blank=True, null=True)
    sharing_text = models.CharField(max_length=140, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_upcoming = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta(object):
        ordering = ['-is_upcoming']
        verbose_name_plural = 'events'


class Track(models.Model):
    event = models.ForeignKey(Event, related_name='event_track', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.URLField()
    datetime = models.DateTimeField()
    address = models.CharField(max_length=200, blank=True, null=True)
    details = models.TextField()
    register_link = models.URLField(blank=True, null=True)
    sharing_text = models.CharField(max_length=140, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.CASCADE)
    is_interaction_active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta(object):
        ordering = ['-datetime']
        verbose_name_plural = 'event tracks'
