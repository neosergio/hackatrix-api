from django.contrib import admin
from .models import Location, Event, Track


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'dates', 'details', 'is_featured', 'is_upcoming', 'is_active')


class TrackAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'datetime', 'details', 'location', 'is_interaction_active', 'is_active')


admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Track, TrackAdmin)
