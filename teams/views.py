from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.core.cache import cache
from teams.base import FullInitializer
from teams.common import generate_identifier
from teams.forms import TeamForm, TeamIdentifierForm
from teams.models import Team, TeamJunction, PendingUser
from django.views.generic.base import ContextMixin
from utils.mixins import GenericDispatchMixin, PaginateObjectMixin, EnableSearchBarMixin
from utils.http import Http400
from utils.base import BaseRedirectFormView
from teams.mixins import InitializeTeamMixin
from django.db import IntegrityError


class TeamHomeView(PaginateObjectMixin, ContextMixin, GenericDispatchMixin, View):
    per_page = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = None
        self.message = None
        self.all_teams = None
        self.ownership_teams = None

    def dispatch(self, request, *args, **kwargs):
        self.errors = self.request.session.pop('errors', None)
        self.message = self.request.session.pop('message', None)

        # First, query the database
        self.all_teams = cache.get(self.request.user)['user_teams']
        self.ownership_teams = self.all_teams.filter(owner=self.request.user)

        # Second, get query params for page
        all_teams_page = self.request.GET.get('at_page', 1)
        ownership_teams_page = self.request.GET.get('ot_page', 1)

        # Third, paginate the objects
        self.all_teams = self.paginate(self.all_teams, all_teams_page)
        self.ownership_teams = self.paginate(self.ownership_teams, ownership_teams_page)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'teams/home/team_home.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_teams': self.all_teams,
                        'ownership_teams': self.ownership_teams,
                        'join_form': TeamIdentifierForm(),
                        'create_form': TeamForm(),
                        'errors': self.errors,
                        'message': self.message})
        return context


class ManageTeam(InitializeTeamMixin, PaginateObjectMixin, ContextMixin, View):
    per_page = 5
    orphans = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = None

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'GET':
            raise Http400
        self.errors = self.request.session.pop('errors', None)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'teams/management/manage_team.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        joined_users_page = self.request.GET.get('u_page', 1)
        joined_users = self.paginate(TeamJunction.objects.filter(team=self.team).only('user'),
                                     joined_users_page)

        context.update({'team': self.team,
                        'owner': self.team.owner.username,
                        'joined_users': joined_users,
                        'errors': self.errors,
                        'is_trusted': self.is_trusted})

        if self.is_trusted:
            pending_users_page = self.request.GET.get('p_page', 1)
            pending_users = self.paginate(PendingUser.objects.filter(team=self.team).only('user'),
                                          pending_users_page)

            context.update({'pending_users': pending_users,
                            'identifier_form': TeamIdentifierForm(initial={'identifier': self.team.identifier}),
                            'name_form': TeamForm(instance=self.team)})
        return context


class CreateTeam(BaseRedirectFormView):
    form_class = TeamForm
    success_url = 'teams:team_home'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.owner = self.request.user
        form.identifier = generate_identifier(form.title)
        form.save()
        TeamJunction.objects.create(team=form, user=self.request.user)
        return self.redirect()


class JoinTeam(BaseRedirectFormView):
    form_class = TeamIdentifierForm
    success_url = 'teams:team_home'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []

    def form_valid(self, form):
        identifier = form.cleaned_data['identifier']

        team = Team.objects.get_or_none(identifier=identifier)
        self.validate_entry(team)

        if self.errors:
            return self.form_invalid(self.errors)

        PendingUser.objects.create(team=team, user=self.request.user)
        self.request.session['message'] = 'You have successfully applied to join this team! ' \
                                          'Your request is pending.'
        return self.redirect()

    def validate_entry(self, team: Team) -> None:
        """
        Validation method. It populates self.errors attribute. Returns None.
        """
        if not team:
            self.errors.append('This identifier does not point to any team!')
            return

        pending = bool(PendingUser.objects.get_or_none(user=self.request.user,
                                                       team=team))
        if pending:
            self.errors.append('Your request is pending.')
            return

        already_joined = bool(TeamJunction.objects.get_or_none(user=self.request.user,
                                                               team=team))
        if already_joined:
            self.errors.append('You are already a member of this Team!')
            return


class AcceptUser(FullInitializer, View):
    admin_only = True
    pending = True

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http400
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user.delete()
        TeamJunction.objects.create(team=self.team, user=self.user.user)
        return redirect(reverse('teams:manage_team', kwargs={'team': self.team}))


class KickUser(FullInitializer, ContextMixin, GenericDispatchMixin, View):
    """
    Here, pending attr is True, because InitializeUserMixin is first looking in TeamJunction
    and then in PendingUser table IF pending is True. IT could be that you are kicking user in a team, but
    still including pending = True.
    """

    admin_only = True
    pending = True

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'teams/management/kick_user.html', context)

    def post(self, request, *args, **kwargs):
        self.user.delete()
        return redirect(reverse('teams:manage_team', kwargs={'team': self.team}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'user': self.user,
                        'button_value': 'Kick'})
        return context


class LeaveTeam(FullInitializer, ContextMixin, GenericDispatchMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'teams/home/leave_team.html', context)

    def post(self, request, *args, **kwargs):
        self.user.delete()
        return redirect('teams:team_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'team': self.team,
                        'button_value': 'Leave'})
        return context


class DeleteTeam(InitializeTeamMixin, ContextMixin, GenericDispatchMixin, View):
    admin_only = True

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'teams/home/team_delete.html', context)

    def post(self, request, *args, **kwargs):
        self.team.delete()
        return redirect('teams:team_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = 'Delete'
        return context


class ChangeTeamIdentifier(InitializeTeamMixin, BaseRedirectFormView):
    admin_only = True
    form_class = TeamIdentifierForm
    success_url = 'teams:manage_team'

    def form_valid(self, form):
        identifier = form.cleaned_data['identifier']

        if self.team.identifier == identifier:
            return self.form_invalid(['You entered the same Team Identifier.'])

        try:
            self.team.identifier = identifier
            self.team.save()
        except IntegrityError:
            return self.form_invalid(['An error occurred. Please try another identifier!'])

        self.team.identifier = identifier
        self.team.save()
        return self.redirect()

    def redirect(self, redirect_kwargs=None):
        return super().redirect({'team': self.team})


class ChangeTeamName(InitializeTeamMixin, BaseRedirectFormView):
    admin_only = True
    form_class = TeamForm
    success_url = 'teams:manage_team'

    def form_valid(self, form):
        name = form.cleaned_data['title']

        if self.team.title == name:
            return self.form_invalid(['You entered the same Team name.'])

        try:
            self.team.title = name
            self.team.save()
        except IntegrityError:
            return self.form_invalid(['An error occurred. Please try another name!'])

        self.team.title = name
        self.team.save()
        return self.redirect()

    def redirect(self, redirect_kwargs=None):
        return super().redirect({'team': self.team})
