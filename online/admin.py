from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import CategoryScore
from .models import Comment
from .models import Evaluation
from .models import EvaluationCommittee
from .models import Evaluator
from .models import Team
from .models import TeamMember


class CategoryScoreAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'percentage', 'score', 'is_committee_score', 'evaluation')


class EvaluationCommitteeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'is_evaluation_closed', 'is_active')


class TeamAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name',
                    'project',
                    'project_description',
                    'evaluation_committee',
                    'is_active')


admin.site.register(CategoryScore, CategoryScoreAdmin)
admin.site.register(Comment)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember)
admin.site.register(EvaluationCommittee, EvaluationCommitteeAdmin)
admin.site.register(Evaluation)
admin.site.register(Evaluator)
