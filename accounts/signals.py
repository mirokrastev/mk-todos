from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from accounts.models import CustomUser, UserProfile
from accounts.common import delete_image
from django.core.cache import cache


@receiver(pre_save, sender=CustomUser)
def check_email(sender, instance, **kwargs):
    instance.email = instance.email or None


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(pre_delete, sender=CustomUser)
def delete_user_avatar(sender, instance, **kwargs):
    profile = UserProfile.objects.get(user=instance)
    picture = profile.avatar.name.split('/')[-1]

    if picture != 'default-user-avatar.jpg':
        delete_image(profile.avatar.path)


@receiver(post_save, sender=UserProfile)
def clear_cache(sender, instance, **kwargs):
    if instance in cache:
        cache.delete(instance)
