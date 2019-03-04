from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Location, Event, Track
from .models import Participant, Registrant


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'dates', 'details', 'is_featured', 'is_upcoming', 'is_active')


class TrackAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'datetime', 'details', 'location', 'is_interaction_active', 'is_active')


class RegistrantAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('full_name', 'email', 'code', 'is_email_sent', 'event')
    search_fields = ['email', 'full_name']


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'linked_datetime')
    search_fields = ['user']


admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Registrant, RegistrantAdmin)
admin.site.register(Participant, ParticipantAdmin)
