from django.shortcuts import render
from django.views import View
from todolist.mixins import GetRequestsMixin, PaginateObjectMixin, FilterTodosMixin


class HomeView(GetRequestsMixin, FilterTodosMixin, PaginateObjectMixin, View):
    def __init__(self):
        super().__init__()
        self.todos = None
        self.message = None

    def dispatch(self, request, *args, **kwargs):
        self.todos = self.get_todos()
        self.message = self.request.session.pop('message', None)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'home.html', context)

    def get_context_data(self):
        return {
            'todos': self.todos,
            'is_paginated': bool(self.todos),
            'message': self.message
        }

    def get_todos(self):
        page, order, word = self.make_query_params()
        obj = self.filter_todos(order, word)
        todos = self.paginate(obj, page)
        return todos


class CompletedTodosHomeView(HomeView):
    def get_todos(self):
        page, order, word = self.make_query_params()
        obj = self.filter_todos(order, word, is_null=False)
        todos = self.paginate(obj, page)
        return todos
