from django.shortcuts import render
from django.views import View
from todolist.models import UserTodo, TeamTodo
from utils.mixins import EnableSearchBarMixin
from utils.http import Http400
from django.core.cache import cache


class TodoHomeView(EnableSearchBarMixin, View):
    ORDER_BY = {'oldest': 'date_created', 'newest': '-date_created'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todos = None
        self.message = None

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'GET':
            raise Http400
        self.todos = self.filter_todos()
        self.message = self.request.session.pop('message', None)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, 'home/home.html', context)

    def filter_todos(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        # page = self.request.GET.get('page', 1)
        order = self.ORDER_BY[self.request.GET.get('order_by', 'newest')]
        keyword = self.request.GET.get('q', None)

        params = {'date_completed__isnull': kwargs.get('isnull', True)}
        if keyword:
            params.update({'title__icontains': keyword})

        user_todos = UserTodo.objects.filter(user=self.request.user, **params).order_by(order)

        user_teams = cache.get(self.request.user)['user_teams']
        team_todos = TeamTodo.objects.filter(team__in=user_teams, **params).order_by(order)

        return {'user': user_todos, 'team': team_todos}

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if not bool(self.todos):
            return context

        context.update({
            'user_todos': self.todos['user'],
            'team_todos': self.todos['team'],
            'message': self.message
        })

        return context


class CompletedTodoHomeView(TodoHomeView):
    def filter_todos(self, **kwargs):
        return super().filter_todos(isnull=False)
