from django.contrib import admin
from teams.models import Team, TeamJunction, PendingUser


class TeamJunctionTabularInline(admin.TabularInline):
    model = TeamJunction
    extra = 0


class PendingUserTabularInline(admin.TabularInline):
    model = PendingUser
    extra = 0


class TeamPanel(admin.ModelAdmin):
    inlines = [
        TeamJunctionTabularInline,
        PendingUserTabularInline
    ]


admin.site.register(Team, TeamPanel)
