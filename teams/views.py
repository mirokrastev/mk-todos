from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import ContextMixin
from teams.common import generate_identifier
from teams.forms import TeamForm, TeamIdentifierForm
from teams.models import Team, TeamJunction
from utils.mixins import GenericDispatchMixin
from teams.mixins import InitializeTeamMixin, InitializeUserMixin
from utils.http import Http400


class TeamHomeView(GenericDispatchMixin, ContextMixin, View):
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
        return render(self.request, 'teams/team_home.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_teams': self.all_teams,
                        'ownership_teams': self.ownership_teams,
                        'join_form': TeamIdentifierForm(),
                        'create_form': TeamForm(),
                        'errors': self.errors})
        return context


class ManageTeam(InitializeTeamMixin, GenericDispatchMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'teams/management/manage_team.html', context)

    def post(self, request, *args, **kwargs):
        if not self.is_trusted:
            raise Http400

        # TODO: IMPLEMENT MULTIPLE FORMS ON ONE URL/VIEW!

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'owner': self.team.owner,
                        'users': [entry.user for entry in TeamJunction.objects.filter(team=self.team)],
                        'identifier_form': TeamIdentifierForm(initial={'identifier': self.team.identifier})})
        return context


class CreateTeam(GenericDispatchMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http400
        self.request.session['errors'] = []
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = TeamForm(self.request.POST)
        if not form.is_valid():
            return self.form_invalid(*form.errors.values())

        form = form.save(commit=False)
        form.owner = self.request.user
        form.identifier = generate_identifier(form.title)
        form.save()
        TeamJunction.objects.create(team=form, user=self.request.user)
        return redirect('teams:team_home')

    def form_invalid(self, list_of_errors=None):
        self.request.session['errors'].extend(list_of_errors or [])
        return redirect('teams:team_home')


class JoinTeam(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http400
        self.request.session['errors'] = []
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = TeamIdentifierForm(self.request.POST)
        if not form.is_valid():
            return self.form_invalid(*form.errors.values())

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
        return redirect('teams:team_home')

    def form_invalid(self, list_of_errors=None):
        self.request.session['errors'].extend(list_of_errors or [])
        return redirect('teams:team_home')


class LeaveTeam(InitializeTeamMixin, InitializeUserMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http400
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user == self.user:
            return redirect('teams:delete_team', kwargs={'team': self.kwargs['team']})
        self.user.delete()
        return redirect('teams:team_home')


class KickUser(InitializeTeamMixin, InitializeUserMixin, ContextMixin, GenericDispatchMixin, View):
    admin_only = True

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'teams/delete/team_delete.html', context)

    def post(self, request, *args, **kwargs):
        self.user.delete()
        return redirect('teams:team_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


class DeleteTeam(InitializeTeamMixin, GenericDispatchMixin, View):
    admin_only = True

    def get(self, request, *args, **kwargs):
        return render(self.request, 'teams/delete/team_delete.html')

    def post(self, request, *args, **kwargs):
        self.team.delete()
        return redirect('teams:team_home')
