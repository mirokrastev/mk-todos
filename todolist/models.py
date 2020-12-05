from django.db import models
from accounts.models import CustomUser


class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name='Task')
    memo = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
