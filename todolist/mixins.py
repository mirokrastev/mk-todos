from django.http import Http404
from teams.models import TeamJunction
from todolist.models import UserTodo, TeamTodo


class GetSingleTodoMixin:
    """
    To return an instance of TeamTodo, in the implementation add team_todo = True.
    To work, you need to pass the team in the url.
    """
    team_todo = False

    def get_object(self, *args, **kwargs):
        todo = self.__get_team_todo() if self.team_todo else self.__get_user_todo()
        slug_kwarg = self.kwargs['todo_title']

        if not todo or todo.slug != slug_kwarg:
            return None
        return todo

    def __get_user_todo(self):
        try:
            return UserTodo.objects.get(pk=self.kwargs['todo_pk'],
                                        user=self.request.user)
        except (UserTodo.DoesNotExist, ValueError):
            return None

    def __get_team_todo(self):
        try:
            team = TeamJunction.objects.get(user=self.request.user, team__slug=self.kwargs['team']).team
            return TeamTodo.objects.get(pk=self.kwargs['todo_pk'],
                                        team=team)
        except (TeamJunction.DoesNotExist, TeamTodo.DoesNotExist, ValueError):
            return None


class InitializeTodoMixin(GetSingleTodoMixin):
    post_only = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def dispatch(self, request, *args, **kwargs):
        self.todo = self.get_object()
        if not self.todo:
            raise Http404
        if self.post_only and not self.request.method == 'POST':
            raise Http404
        return super().dispatch(request, *args, **kwargs)
