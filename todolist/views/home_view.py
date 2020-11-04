from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from todolist.views.mixins import GetRequestMixin, PaginatePageMixin
from todolist.views.todo_creation.main import MakeGenericTodos, MakeSearchTodos


class HomeView(GetRequestMixin, PaginatePageMixin, View):
    ORDER_BY = {'oldest': 'date_created', 'newest': '-date_created'}

    def __init__(self):
        super().__init__()
        self.todos = None

    def get(self, request):
        message = self.request.session.pop('message', None)

        if self.request.user.is_authenticated:
            self.todos = self.authorised_action()

        context = {
            'todos': self.todos,
            'is_paginated': True if self.todos else False,
            'message': message
        }
        return render(request, 'home.html', context)

    def post(self, request):
        self.request.method = 'GET'
        return self.get(request)

    def authorised_action(self):
        page, order, _ = self.make_query_params()

        todos = self.paginate(MakeGenericTodos.make_todos(self, order), page)
        return todos


class SearchTodosHomeView(LoginRequiredMixin, HomeView):
    def authorised_action(self):
        page, order, word = self.make_query_params()

        todos = self.paginate(MakeSearchTodos.make_todos(self, order, word), page)
        return todos


class CompletedTodosHomeView(LoginRequiredMixin, HomeView):
    def authorised_action(self):
        page, order, _ = self.make_query_params()

        todos = self.paginate(MakeGenericTodos.make_todos(self, order, False), page)
        return todos