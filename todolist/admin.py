from django.contrib import admin
from .models import UserTodo, TeamTodo


class UserTodoPanel(admin.ModelAdmin):
    list_display = ('title', 'user')
    search_fields = ('title', 'user__username')


class TeamTodoPanel(admin.ModelAdmin):
    list_display = ('title', 'team')
    search_fields = ('title', 'team__title')


admin.site.register(UserTodo, UserTodoPanel)
admin.site.register(TeamTodo, TeamTodoPanel)
