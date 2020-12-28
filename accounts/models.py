from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)


class UserProfile(models.Model):
    bio = models.CharField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/user-profiles', default='/images/default-user-avatar.jpg')
    dark_mode = models.BooleanField(default=False)
    user = models.OneToOneField(db_index=True, to=CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
