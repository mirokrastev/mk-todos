from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task
from django.utils import timezone


def home_view(request, isnull=True, message=None):
    ORDER_BY = {'ascending': 'date_created', 'descending': '-date_created'}
    todos = None

    if request.user.is_authenticated:
        order = ORDER_BY[request.GET.get('order_by', 'descending')]
        todos = list(
            Task.objects.filter(user=request.user, date_completed__isnull=isnull).order_by(order)
        )
        if todos:
            todos[0].is_first = True
    return render(request, 'home.html', {'todos': todos, 'message': message})


def get_object(request, task_pk):
    try:
        return Task.objects.get(pk=task_pk, user=request.user)
    except (Task.DoesNotExist, ValueError):
        return None


@login_required
def search_view(request):
    word = request.GET['search']
    todos = Task.objects.filter(user=request.user, title__icontains=word)
    return render(request, 'home.html', {'todos': todos})


@login_required
def completed_todos_view(request):
    return home_view(request, isnull=False)


@login_required
def create_todo_view(request):
    error = None

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if len(form['title'].data) <= 50:
            new = form.save(commit=False)
            new.user = request.user
            new.save()

            return redirect('home')

        error = 'Please submit only valid data.'
    form = TaskForm()
    return render(request, 'todolist/create_todo.html', {'form': form, 'error': error})


@login_required
def detailed_todo_view(request, task_pk):
    task = get_object(request, task_pk)
    error = None

    if not task:
        return home_view(request, message='Invalid task.')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
        error = 'Please submit only valid data.'

    task_paragraph = TaskForm(instance=task)
    return render(request, 'todolist/detailed_todo.html', {'object': task,
                                                           'task': task_paragraph, 'error': error})


@login_required
def complete_todo_view(request, task_pk):
    task = get_object(request, task_pk)
    if not task:
        return home_view(request, message='Invalid task.')

    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return home_view(request, message=f'You completed task {task.title}!')
    return redirect(home_view)


@login_required
def delete_todo_view(request, task_pk):
    task = get_object(request, task_pk)
    if not task:
        return home_view(request, message='Invalid task.')

    if request.method == 'POST':
        task.delete()
        return home_view(request, message=f'You deleted task {task.title}!')
    return redirect(home_view)
