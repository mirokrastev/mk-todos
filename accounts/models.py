from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from accounts.common import delete_image


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class UserProfile(models.Model):
    bio = models.CharField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/user-profiles', default='/images/default-user-avatar.jpg')
    dark_mode = models.BooleanField(default=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    @staticmethod
    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @staticmethod
    @receiver(pre_delete, sender=CustomUser)
    def delete_user_avatar(sender, instance, **kwargs):
        profile = UserProfile.objects.get(user=instance)
        picture = profile.avatar.name.split('/')[-1]

        if picture != 'default-user-avatar.jpg':
            delete_image(profile.avatar.path)

    def __str__(self):
        return self.user.username
