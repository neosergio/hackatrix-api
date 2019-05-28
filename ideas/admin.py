from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Idea, IdeaTeamMember


class IdeaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title',
                    'author',
                    'event',
                    'is_valid',
                    'is_active',
                    'max_number_of_participants',
                    'created_at',
                    'modified_at')


class IdeaTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('idea', 'member')


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaTeamMember, IdeaTeamMemberAdmin)
