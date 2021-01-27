from teams.models import Team, TeamJunction
from django.http import Http404


class InitializeTeamMixin:
    admin_only = False

    def __init__(self):
        super().__init__()
        self.team = None
        self.is_trusted = False

    def dispatch(self, request, *args, **kwargs):
        self.team = Team.objects.get_or_none(title=self.kwargs['team'])
        if not self.team:
            raise Http404

        self.is_trusted = self.team.owner == self.request.user

        if self.admin_only:
            if not self.is_trusted:
                raise Http404
        return super().dispatch(request, *args, **kwargs)


class InitializeUserMixin:
    """
    This Mixin requires InitializeTeamMixin to work.
    NOTE: The correct inheritance order is InitializeTeamMixin, InitializeUserMixin!
    """
    def __init__(self):
        super().__init__()
        self.user = None

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('user', None) or self.request.user.username
        self.user = TeamJunction.objects.get_or_none(team=self.team, user__username=username)

        if not self.user:
            raise Http404

        if self.admin_only:
            if self.is_trusted:
                raise Http404
        return super().dispatch(request, *args, **kwargs)