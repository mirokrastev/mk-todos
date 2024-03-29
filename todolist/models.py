from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import CustomUser
from teams.models import Team


class BaseTodo(models.Model):
    title = models.CharField(db_index=True, max_length=50, verbose_name='Task')
    slug = models.SlugField(blank=True, allow_unicode=True)
    memo = models.TextField(blank=True)
    date_created = models.DateTimeField(db_index=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class UserTodo(BaseTodo):
    user = models.ForeignKey(db_index=True, to=CustomUser, on_delete=models.CASCADE)


class TeamTodo(BaseTodo):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
