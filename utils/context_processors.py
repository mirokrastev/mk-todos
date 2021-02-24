from django.core.cache import cache


def generic(request):
    if request.user.is_authenticated:
        cache_dict = cache.get(request.user)
        return {'dark_mode': cache_dict['userprofile'].dark_mode,
                'has_team': bool(cache_dict['user_teams'])}
    return {'dark_mode': False, 'has_team': False}
