from django.contrib import admin

from .models import Idea, IdeaTeamMember
from .models import JuryAssessments, JuryAssessmentIdea, ModeratorAssesssment, ModeratorAssessmentIdea


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'event', 'is_valid', 'max_number_of_participants')


class IdeaTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('idea', 'member')


class JuryAssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'weight')


class JuryAssessmentIdeaAdmin(admin.ModelAdmin):
    list_display = ('idea', 'jury', 'value')


class ModeratorAssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'weight')


class ModeratorAssessmentIdeaAdmin(admin.ModelAdmin):
    list_display = ('idea', 'jury', 'value')


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaTeamMember, IdeaTeamMemberAdmin)
admin.site.register(JuryAssessments, JuryAssessmentAdmin)
admin.site.register(JuryAssessmentIdea, JuryAssessmentIdeaAdmin)
admin.site.register(ModeratorAssesssment, ModeratorAssessmentAdmin)
admin.site.register(ModeratorAssessmentIdea, ModeratorAssessmentIdeaAdmin)
