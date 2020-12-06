from django.http import Http404
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, UpdateView
from todolist.forms import TaskForm
from django.utils import timezone
from todolist.mixins import GetSingleTodoMixin, InitializeTodoMixin


class CreateTodo(CreateView):
    form_class = TaskForm
    context_object_name = 'form'
    template_name = 'todolist/create_todo.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return redirect('home')


class CompleteTodo(InitializeTodoMixin, View):
    def post(self, request, *args, **kwargs):
        self.task.date_completed = timezone.now()
        self.task.save()
        self.request.session['message'] = f'You completed {self.task.title}!'
        return redirect('home')


class ReopenTodo(InitializeTodoMixin, View):
    def post(self, request, *args, **kwargs):
        self.task.date_completed = None
        self.task.date_created = timezone.now()
        self.task.save()
        self.request.session['message'] = f'You reopened {self.task.title}!'
        return redirect('home')


class DeleteTodo(InitializeTodoMixin, View):
    def post(self, request, *args, **kwargs):
        self.task.delete()
        self.request.session['message'] = f'You deleted {self.task.title}!'
        return redirect('home')


class DetailedTodo(GetSingleTodoMixin, UpdateView):
    form_class = TaskForm
    context_object_name = 'form'
    template_name = 'todolist/detailed_todo.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def dispatch(self, request, *args, **kwargs):
        self.todo = self.get_object()
        if self.request.method not in ('GET', 'POST') or not self.todo:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

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
