from django.core.cache import cache
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView, UpdateView
from todolist.forms import UserTodoForm, TeamTodoForm
from django.utils import timezone
from todolist.mixins import InitializeTodoMixin
from utils.http import Http400
from utils.mixins import GenericDispatchMixin


class UserTodoCreation(GenericDispatchMixin, FormView):
    template_name = 'todolist/create todo/create_todo.html'
    form_class = UserTodoForm

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return redirect('home')


class TeamTodoCreation(GenericDispatchMixin, FormView):
    template_name = 'todolist/create todo/create_todo.html'
    form_class = TeamTodoForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = None

    def dispatch(self, request, *args, **kwargs):
        self.queryset = cache.get(self.request.user)['user_teams']
        if not self.queryset:
            raise Http400
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['team'].queryset = self.queryset
        return form


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


class UserDetailedTodo(BaseDetailedTodo):
    form_class = UserTodoForm


class TeamDetailedTodo(BaseDetailedTodo):
    form_class = TeamTodoForm
    team_todo = True

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields.pop('team')
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_todo'] = True
        return context
