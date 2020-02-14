from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Location, Event, Track, TrackItemAgenda
from .models import Registrant
from .models import Attendance, RegistrantAttendance
from .models import Team, TeamMember


class LocationAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')


class EventAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'image', 'dates', 'details', 'is_featured', 'is_upcoming', 'is_active')


class TrackAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('event', 'title', 'datetime', 'details', 'location', 'is_interaction_active', 'is_active')


class TrackItemAgendaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('track', 'time', 'text')


class RegistrantAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('full_name', 'email', 'code', 'is_email_sent', 'event')
    search_fields = ['email', 'full_name', 'code']


class AttendanceAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'event', 'available_from', 'due_date', 'is_active', 'max_capacity')


class RegistrantAttendanceAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('attendance', 'registrant', 'registered_by', 'registered_at')


class TeamAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'event', 'description', 'table', 'is_valid', 'is_active')
    search_fields = ['title', 'table']


class TeamMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('full_name', 'is_active', 'team')
    search_fields = ['full_name', 'team__name']


admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(TrackItemAgenda, TrackItemAgendaAdmin)
admin.site.register(Registrant, RegistrantAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(RegistrantAttendance, RegistrantAttendanceAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
