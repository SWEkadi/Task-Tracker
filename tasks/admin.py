from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'status', 'is_completed', 'created_at')
    list_filter = ('priority', 'status', 'is_completed', 'created_at')
    search_fields = ('title', 'description', 'user__username')