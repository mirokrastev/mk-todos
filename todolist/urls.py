from django.urls import path
from todolist.views import generic_views as views
from todolist.views.home_view import CompletedTodosHomeView

urlpatterns = [
    path('create', views.create_todo_view, name='create'),
    path('completed', CompletedTodosHomeView.as_view(), name='completed_todos'),

    path('<int:task_pk>/<str:name>', views.detailed_todo_view, name='detailed_todo'),
    path('<int:task_pk>/<str:name>/complete', views.complete_todo_view, name='complete_todo'),
    path('<int:task_pk>/<str:name>/reopen', views.reopen_todo_view, name='reopen_todo'),
    path('<int:task_pk>/<str:name>/delete', views.delete_todo_view, name='delete_todo'),
]
