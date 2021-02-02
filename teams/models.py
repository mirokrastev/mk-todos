from django.db import models
from accounts.models import CustomUser
from teams.managers import TeamManager


class Team(models.Model):
    title = models.CharField(db_index=True, max_length=25, unique=True, verbose_name='Team')
    identifier = models.CharField(db_index=True, unique=True, max_length=20)
    owner = models.ForeignKey(db_index=True, to=CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    objects = TeamManager()


class TeamJunction(models.Model):
    team = models.ForeignKey(db_index=True, to=Team, on_delete=models.CASCADE)
    user = models.ForeignKey(db_index=True, to=CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}:{self.team.title}'

    objects = TeamManager()
