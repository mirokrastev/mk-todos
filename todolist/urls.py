from django.urls import path
from todolist.views.todo import generic, user, team
from django.contrib.auth.decorators import login_required
from todolist.views.home import CompletedTodoHomeView
from teams.urls import urlpatterns as teams_urlpatterns

app_name = 'todo'

urlpatterns = [
    path('create/', login_required(user.UserTodoCreation.as_view()), name='user_create_todo'),
    path('completed/', login_required(CompletedTodoHomeView.as_view()), name='completed_todos'),

    # User Todos Management
    path('<int:todo_pk>/<slug:todo_title>/', login_required(user.UserDetailedTodo.as_view()),
         name='user_detailed_todo'),

    path('<int:todo_pk>/<slug:todo_title>/complete/', login_required(generic.CompleteTodo.as_view()),
         name='user_complete_todo'),

    path('<int:todo_pk>/<slug:todo_title>/reopen/', login_required(generic.ReopenTodo.as_view()),
         name='user_reopen_todo'),

    path('<int:todo_pk>/<slug:todo_title>/delete/', login_required(generic.DeleteTodo.as_view()),
         name='user_delete_todo'),
]

teams_urlpatterns += [
    # Team Todos Management
    path('todo/create/', login_required(team.TeamTodoCreation.as_view()),
         name='team_todo_create'),

    path('<slug:team>/todo/<int:todo_pk>/<slug:todo_title>/', login_required(team.TeamDetailedTodo.as_view()),
         name='team_detailed_todo'),

    path('<slug:team>/todo/<int:todo_pk>/<slug:todo_title>/complete/',login_required(generic.CompleteTodo.as_view()),
         name='team_complete_todo'),

    path('<slug:team>/todo/<int:todo_pk>/<slug:todo_title>/reopen/', login_required(generic.ReopenTodo.as_view()),
         name='team_reopen_todo'),

    path('<slug:team>/todo/<int:todo_pk>/<slug:todo_title>/delete/', login_required(generic.DeleteTodo.as_view()),
         name='team_delete_todo'),
]
