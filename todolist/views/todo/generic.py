from django.shortcuts import redirect
from django.views import View
from django.views.generic import UpdateView
from django.utils import timezone
from todolist.mixins import InitializeTodoMixin
from utils.mixins import GenericDispatchMixin


class CompleteTodo(InitializeTodoMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if 'team' in self.kwargs:
            self.team_todo = True
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.todo.date_completed = timezone.now()
        self.todo.save()
        self.request.session['message'] = f'You completed {self.todo.title}!'
        return redirect('home')


class ReopenTodo(InitializeTodoMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if 'team' in self.kwargs:
            self.team_todo = True
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.todo.date_completed = None
        self.todo.date_created = timezone.now()
        self.todo.save()
        self.request.session['message'] = f'You reopened {self.todo.title}!'
        return redirect('home')


class DeleteTodo(InitializeTodoMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if 'team' in self.kwargs:
            self.team_todo = True
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.todo.delete()
        self.request.session['message'] = f'You deleted {self.todo.title}!'
        return redirect('home')


class BaseDetailedTodo(InitializeTodoMixin, GenericDispatchMixin, UpdateView):
    post_only = False
    form_class = None
    template_name = 'todolist/detailed todo/main.html'

    def form_valid(self, form):
        form.save()
        return redirect('home')

    def form_invalid(self, form):
        context = self.get_context_data()
        context['error'] = 'Please submit only valid data.'
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.todo
        return context
