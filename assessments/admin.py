from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Assessment, ProjectAssessment, RegistrantAssessment, RegistrantComment
from .models import TeamAssessment, TeamAssessmentResults, FinalResult


class AssessmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title',
                    'weight',
                    'is_for_jury',
                    'is_for_evaluation_committee',
                    'is_for_HR',
                    'is_for_team_leader')


class ProjectAssessmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('assessment',
                    'idea',
                    'evaluator',
                    'value',
                    'created_at',
                    'modified_at')


class RegistrantAssessmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('assessment',
                    'registrant',
                    'evaluator',
                    'value',
                    'created_at',
                    'modified_at')


class RegistrantCommentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('registrant', 'comment', 'comment_by', 'created_at', 'modified_at')


class TeamAssessmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('team', 'evaluator', 'has_been_assessed')


class TeamAssessmentResultsAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('assessment', 'team', 'evaluator', 'value', 'created_at', 'modified_at')


class FinalResultAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('team', 'score', 'type')
    search_fields = ['team__name']


admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(ProjectAssessment, ProjectAssessmentAdmin)
admin.site.register(RegistrantAssessment, RegistrantAssessmentAdmin)
admin.site.register(RegistrantComment, RegistrantCommentAdmin)
admin.site.register(TeamAssessment, TeamAssessmentAdmin)
admin.site.register(TeamAssessmentResults, TeamAssessmentResultsAdmin)
admin.site.register(FinalResult, FinalResultAdmin)
