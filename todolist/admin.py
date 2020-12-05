from django.contrib import admin
from .models import Task


class TaskPanel(admin.ModelAdmin):
    list_display = ('title', 'user')
    search_fields = ('title', 'user__username')


admin.site.register(Task, TaskPanel)
