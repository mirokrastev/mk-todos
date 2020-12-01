from accounts.models import UserProfile


def dark_mode(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user=request.user)
        return {'dark_mode': user.dark_mode}
    return {'dark_mode': False}
