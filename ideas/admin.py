from django.contrib import admin

from .models import Idea, IdeaTeamMember


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'event', 'is_valid', 'max_number_of_participants')


class IdeaTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('idea', 'member')


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaTeamMember, IdeaTeamMemberAdmin)
