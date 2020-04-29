from django.contrib import admin

from .models import CategoryScore
from .models import Comment
from .models import Evaluation
from .models import EvaluationCommittee
from .models import Team
from .models import TeamMember
from .models import Evaluator


class EvaluationCommitteeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_evaluation_closed', 'is_active')


admin.site.register(CategoryScore)
admin.site.register(Comment)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(EvaluationCommittee, EvaluationCommitteeAdmin)
admin.site.register(Evaluation)
admin.site.register(Evaluator)
