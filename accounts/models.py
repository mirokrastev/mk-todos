from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class UserProfile(models.Model):
    bio = models.CharField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/user-profiles', default='/images/default-user-avatar.jpg')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    @staticmethod
    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    def __str__(self):
        return self.user.username
