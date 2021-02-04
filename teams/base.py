from teams.mixins import InitializeTeamMixin, InitializeUserMixin


class FullInitializer(InitializeTeamMixin, InitializeUserMixin):
    """
    Simple class to reduce the number of direct mixin inheritance. It is not a View,
    so you should give it an interface to work! It is just initializing the team and team's user.
    """
    pass
