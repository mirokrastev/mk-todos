from django.core.cache import cache
from django.shortcuts import redirect
from django.views.generic import FormView
from todolist.forms import TeamTodoForm
from todolist.views.todo.generic import BaseDetailedTodo
from utils.http import Http400
from utils.mixins import GenericDispatchMixin


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
