from django.contrib import admin
from .models import CustomUser, UserProfile


class CustomUserFields(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')


admin.site.register(CustomUser, CustomUserFields)
admin.site.register(UserProfile)
