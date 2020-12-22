from django.urls import path
from todolist.views import generic_views as views
from django.contrib.auth.decorators import login_required
from todolist.views.home_view import CompletedTodosHomeView

app_name = 'todo'

urlpatterns = [
    path('create', login_required(views.CreateTodo.as_view()), name='create_todo'),
    path('completed', login_required(CompletedTodosHomeView.as_view()), name='completed_todos'),

    path('<int:task_pk>/<str:name>', login_required(views.DetailedTodo.as_view()), name='detailed_todo'),
    path('<int:task_pk>/<str:name>/complete', login_required(views.CompleteTodo.as_view()), name='complete_todo'),
    path('<int:task_pk>/<str:name>/reopen', login_required(views.ReopenTodo.as_view()), name='reopen_todo'),
    path('<int:task_pk>/<str:name>/delete', login_required(views.DeleteTodo.as_view()), name='delete_todo'),
]
