from django.db import models
from django.utils.crypto import get_random_string


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


class Registrant(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    is_code_used = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def generate_code(self):
        code = get_random_string(6, "abcdefghkmnpqrstuvwxyz023456789")
        return code

    def save(self, *args, **kwargs):
        if self.code is None:
            self.code = self.generate_code()
        super(Registrant, self).save(*args, **kwargs)


class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    code_used = models.CharField(max_length=6, blank=True, null=True)
    linked_datetime = models.DateTimeField(auto_now_add=True)
