from django.shortcuts import render
from django.views import View
from todolist.mixins import GetRequestsMixin, PaginateObjectMixin, FilterTodosMixin
from utils.mixins import EnableSearchBarMixin
from utils.http import Http400


class HomeView(EnableSearchBarMixin, GetRequestsMixin, FilterTodosMixin, PaginateObjectMixin, View):
    def __init__(self):
        super().__init__()
        self.todos = None
        self.message = None

    def dispatch(self, request, *args, **kwargs):
        # if not self.request.method == 'GET':
        #     raise Http400
        self.todos = self.get_todos()
        self.message = self.request.session.pop('message', None)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'home/home.html', context)

    def get_todos(self):
        page, order, word = self.make_query_params()
        obj = self.filter_todos(order, word)
        todos = self.paginate(obj, page)
        return todos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'todos': self.todos,
            'is_paginated': bool(self.todos),
            'message': self.message})
        return context


class CompletedTodosHomeView(HomeView):
    def get_todos(self):
        page, order, word = self.make_query_params()
        obj = self.filter_todos(order, word, is_null=False)
        todos = self.paginate(obj, page)
        return todos
