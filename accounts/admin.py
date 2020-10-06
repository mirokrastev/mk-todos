from django.contrib import admin
from .models import CustomUser


class CustomUserFields(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')


admin.site.register(CustomUser, CustomUserFields)
