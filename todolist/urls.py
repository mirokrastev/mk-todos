from django.urls import path
from todolist.views import create_todo_view, detailed_todo_view, delete_todo_view, \
                           completed_todos_view, complete_todo_view, reopen_todo_view

urlpatterns = [
    path('create', create_todo_view, name='create'),
    path('completed', completed_todos_view, name='completed_todos'),

    path('<int:task_pk>/', detailed_todo_view, name='detailed_todo'),
    path('<int:task_pk>/complete', complete_todo_view, name='complete_todo'),
    path('<int:task_pk>/reopen', reopen_todo_view, name='reopen_todo'),
    path('<int:task_pk>/delete', delete_todo_view, name='delete_todo'),
]
