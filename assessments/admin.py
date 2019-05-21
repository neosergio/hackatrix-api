from django.contrib import admin
from .models import Assessment, ProjectAssessment, RegistrantAssessment, RegistrantComment


class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'weight',
                    'is_for_jury',
                    'is_for_evaluation_committee',
                    'is_for_HR',
                    'is_for_team_leader')


class ProjectAssessmentAdmin(admin.ModelAdmin):
    list_display = ('assessment',
                    'idea',
                    'evaluator',
                    'value',
                    'created_at',
                    'modified_at')


class RegistrantAssessmentAdmin(admin.ModelAdmin):
    list_display = ('assessment',
                    'registrant',
                    'evaluator',
                    'value',
                    'created_at',
                    'modified_at')


class RegistrantCommentAdmin(admin.ModelAdmin):
    list_display = ('registrant', 'comment', 'comment_by', 'created_at', 'modified_at')


admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(ProjectAssessment, ProjectAssessmentAdmin)
admin.site.register(RegistrantAssessment, RegistrantAssessmentAdmin)
admin.site.register(RegistrantComment, RegistrantCommentAdmin)
