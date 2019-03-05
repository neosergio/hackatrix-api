from django.contrib import admin

from .models import Idea, IdeaParticipant


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'event')


class IdeaParticipantAdmin(admin.ModelAdmin):
    list_display = ('idea', 'participant')


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaParticipant, IdeaParticipantAdmin)
