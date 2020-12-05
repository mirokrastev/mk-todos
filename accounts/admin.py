from django.contrib import admin
from todolist.models import Task
from .models import CustomUser, UserProfile


class TaskTabularInline(admin.TabularInline):
    model = Task
    extra = 0


class CustomUserPanel(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    search_fields = ('username', 'email')

    inlines = (TaskTabularInline,)


class UserProfilePanel(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)


admin.site.register(CustomUser, CustomUserPanel)
admin.site.register(UserProfile, UserProfilePanel)
