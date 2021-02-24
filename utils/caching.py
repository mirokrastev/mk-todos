from django.core.cache import cache
from accounts.models import UserProfile
from teams.models import TeamJunction, Team


class CacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user not in cache:
            teams_id = (team.team.id for team in TeamJunction.objects.filter(user=request.user))
            user_teams = Team.objects.filter(id__in=teams_id)

            cache.set(request.user, {'userprofile': UserProfile.objects.get(user=request.user),
                                     'user_teams': user_teams}, 300)
            print('caching')
        response = self.get_response(request)
        return response
