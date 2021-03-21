from django.shortcuts import redirect
from django.views.generic import FormView
from todolist.forms import UserTodoForm
from todolist.views.todo.generic import BaseDetailedTodo
from utils.mixins import GenericDispatchMixin


class UserTodoCreation(GenericDispatchMixin, FormView):
    template_name = 'todolist/create todo/create_todo.html'
    form_class = UserTodoForm

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return redirect('home')


class UserDetailedTodo(BaseDetailedTodo):
    form_class = UserTodoForm
