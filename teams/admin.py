from django.contrib import admin
from teams.models import Team, TeamJunction


class TeamJunctionTabularInline(admin.TabularInline):
    model = TeamJunction
    extra = 0


class TeamPanel(admin.ModelAdmin):
    inlines = [
        TeamJunctionTabularInline
    ]


admin.site.register(Team, TeamPanel)
