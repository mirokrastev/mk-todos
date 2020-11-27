from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from todolist.forms import TaskForm
from todolist.models import Task
from django.utils import timezone


def get_object(request, task_pk):
    try:
        return Task.objects.get(pk=task_pk, user=request.user)
    except (Task.DoesNotExist, ValueError):
        return None


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
def detailed_todo_view(request, task_pk, name, error=None):
    task = get_object(request, task_pk)
    if not task:
        return Http404

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
def complete_todo_view(request, task_pk, name):
    task = get_object(request, task_pk)
    if not task:
        return Http404

    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        request.session['message'] = f'You completed task {task.title}!'
    return redirect('home')


@login_required
def reopen_todo_view(request, task_pk, name):
    task = get_object(request, task_pk)
    if not task:
        return Http404

    if request.method == 'POST':
        task.date_completed = None
        task.save()
        request.session['message'] = f'You reopened task {task.title}!'
        return redirect('home')
    return detailed_todo_view(request, task_pk, error='Please submit only valid data.')


@login_required
def delete_todo_view(request, task_pk, name):
    task = get_object(request, task_pk)
    if not task:
        return Http404

    if request.method == 'POST':
        task.delete()
        request.session['message'] = f'You deleted task {task.title}!'
    return redirect('home')
