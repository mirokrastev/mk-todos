from accounts.models import UserProfile
from django.core.cache import cache


def dark_mode(request):
    if request.user.is_authenticated:
        if request.user not in cache:
            cache.set(request.user, UserProfile.objects.get(user=request.user), 300)
        return {'dark_mode': cache.get(request.user).dark_mode}
    return {'dark_mode': False}
