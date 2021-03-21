from django.shortcuts import render
from django.views import View
from todolist.models import UserTodo, TeamTodo
from utils.mixins import EnableSearchBarMixin, PaginateObjectMixin
from utils.http import Http400
from django.core.cache import cache
from typing import Dict, Union


class TodoHomeView(EnableSearchBarMixin, PaginateObjectMixin, View):
    ORDER_BY = {'oldest': 'date_created', 'newest': '-date_created'}
    per_page = 4
    orphans = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todos: Union[Dict[str, object], None] = None
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

    def filter_todos(self, **kwargs) -> Union[Dict[str, object], None]:
        """
        this method filters the todos, paginates them and returns them.
        If the user is not authenticated, None is returned.

        This method could return two possible data types: Dictionary with two key-value OR None.
        """
        if not self.request.user.is_authenticated:
            return None

        user_todo_page = self.request.GET.get('u_page', 1)
        team_todo_page = self.request.GET.get('t_page', 1)

        order = self.ORDER_BY[self.request.GET.get('order_by', 'newest')]
        keyword = self.request.GET.get('q', None)

        params = {'date_completed__isnull': kwargs.get('isnull', True)}
        if keyword:
            params.update({'title__icontains': keyword})

        user_todos = UserTodo.objects.filter(user=self.request.user, **params).order_by(order)

        user_teams = cache.get(self.request.user)['user_teams']
        team_todos = TeamTodo.objects.filter(team__in=user_teams, **params).order_by(order)

        return {'user': self.paginate(user_todos, user_todo_page),
                'team': self.paginate(team_todos, team_todo_page, per_page=3, orphans=0)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if not bool(self.todos):
            return context

        context.update({
            'user_todos': self.todos['user'],
            'team_todos': self.todos['team'],
            'message': self.message,
            'is_paginated': True,
        })

        return context


class CompletedTodoHomeView(TodoHomeView):
    def filter_todos(self, **kwargs):
        return super().filter_todos(isnull=False)
