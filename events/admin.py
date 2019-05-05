from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Location, Event, Track, TrackItemAgenda
from .models import Registrant
from .models import Attendance, RegistrantAttendance
from .models import HRAssessment, HRAssessmentRegistrant


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'dates', 'details', 'is_featured', 'is_upcoming', 'is_active')


class TrackAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'datetime', 'details', 'location', 'is_interaction_active', 'is_active')


class TrackItemAgendaAdmin(admin.ModelAdmin):
    list_display = ('track', 'time', 'text')


class RegistrantAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('full_name', 'email', 'code', 'is_email_sent', 'event')
    search_fields = ['email', 'full_name', 'code']


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'available_from', 'due_date', 'is_active')


class RegistrantAttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance', 'registrant', 'registered_by', 'registered_at')


class HRAssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'weight')


class HRAssessmentRegistrantAdmin(admin.ModelAdmin):
    list_display = ('registrant', 'evaluator', 'value')


admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(TrackItemAgenda, TrackItemAgendaAdmin)
admin.site.register(Registrant, RegistrantAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(RegistrantAttendance, RegistrantAttendanceAdmin)
admin.site.register(HRAssessment, HRAssessmentAdmin)
admin.site.register(HRAssessmentRegistrant, HRAssessmentRegistrantAdmin)
