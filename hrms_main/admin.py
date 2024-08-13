# hrms_main/admin.py

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model

User = get_user_model()

class LogEntryAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super(LogEntryAdmin, self).__init__(*args, **kwargs)
        self.list_display = (
            'action_time', 'user', 'content_type', 'object_id', 'object_repr',
            'action_flag', 'change_message'
        )

    def get_queryset(self, request):
        qs = super(LogEntryAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser and obj is not None and obj.user != request.user:
            return False
        return super(LogEntryAdmin, self).has_change_permission(request, obj=obj)

admin.site.register(LogEntry, LogEntryAdmin)
