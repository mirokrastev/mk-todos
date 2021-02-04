from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from teams.base import FullInitializer
from teams.common import generate_identifier
from teams.forms import TeamForm, TeamIdentifierForm
from teams.models import Team, TeamJunction
from django.views.generic.base import ContextMixin
from utils.mixins import GenericDispatchMixin
from utils.http import Http400
from utils.base import BaseRedirectFormView
from teams.mixins import InitializeTeamMixin
from django.db import IntegrityError


class TeamHomeView(ContextMixin, GenericDispatchMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_teams = None
        self.ownership_teams = None
        self.errors = None

    def dispatch(self, request, *args, **kwargs):
        self.all_teams = TeamJunction.objects.filter(user=self.request.user)
        self.ownership_teams = [team
                                for team in self.all_teams
                                if team.team.owner == self.request.user]
        self.errors = self.request.session.pop('errors', None)
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
                        'errors': self.errors})
        return context


class ManageTeam(FullInitializer, ContextMixin, View):
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
        context.update({'team': self.team,
                        'owner': self.team.owner,
                        'users': [entry.user for entry in TeamJunction.objects.filter(team=self.team)],
                        'errors': self.errors,
                        'is_trusted': self.is_trusted})

        if self.is_trusted:
            context.update({'identifier_form': TeamIdentifierForm(initial={'identifier': self.team.identifier}),
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

    def form_valid(self, form):
        identifier = form.cleaned_data['identifier']

        team = Team.objects.get_or_none(identifier=identifier)
        already_joined = bool(TeamJunction.objects.get_or_none(team=team, user=self.request.user))

        if not team or already_joined:
            errors = []
            if not team:
                errors.append('This identifier does not point to any team!')
            if already_joined:
                errors.append('You are already a member of this team!')
            return self.form_invalid(errors)

        TeamJunction.objects.create(team=team, user=self.request.user)
        return self.redirect()


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


class KickUser(FullInitializer, ContextMixin, GenericDispatchMixin, View):
    admin_only = True

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
