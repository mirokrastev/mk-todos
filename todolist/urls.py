from django.urls import path
from todolist.views import generic_views as views
from django.contrib.auth.decorators import login_required
from todolist.views.home_view import CompletedTodoHomeView
from teams.urls import urlpatterns as teams_urlpatterns

app_name = 'todo'

urlpatterns = [
    path('create/', login_required(views.UserTodoCreation.as_view()), name='user_create_todo'),
    path('completed/', login_required(CompletedTodoHomeView.as_view()), name='completed_todos'),
    # TODO: REFACTOR <STR:NAME> TO TODO_TITLE AND <INT:TASK_PK> TO TODO_PK!
    # User Todos Management
    path('<int:task_pk>/<str:name>/', login_required(views.UserDetailedTodo.as_view()),
         name='user_detailed_todo'),

    path('<int:task_pk>/<str:name>/complete/', login_required(views.CompleteTodo.as_view()),
         name='user_complete_todo'),

    path('<int:task_pk>/<str:name>/reopen/', login_required(views.ReopenTodo.as_view()),
         name='user_reopen_todo'),

    path('<int:task_pk>/<str:name>/delete/', login_required(views.DeleteTodo.as_view()),
         name='user_delete_todo'),
]

teams_urlpatterns += [
    # Team Todos Management
    path('todo/create/', login_required(views.TeamTodoCreation.as_view()),
         name='team_todo_create'),

    path('<str:team>/todo/<int:task_pk>/<str:name>/', login_required(views.TeamDetailedTodo.as_view()),
         name='team_detailed_todo'),

    path('<str:team>/todo/<int:task_pk>/<str:name>/complete/', login_required(views.CompleteTodo.as_view()),
         name='team_complete_todo'),

    path('<str:team>/todo/<int:task_pk>/<str:name>/reopen/', login_required(views.ReopenTodo.as_view()),
         name='team_reopen_todo'),

    path('<str:team>/todo/<int:task_pk>/<str:name>/delete/', login_required(views.DeleteTodo.as_view()),
         name='team_delete_todo'),
]
