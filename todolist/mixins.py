from django.core.paginator import Paginator
from django.http import Http404
from teams.models import TeamJunction
from todolist.models import UserTodo, TeamTodo


class PaginateObjectMixin:
    per_page = None

    def paginate(self, obj, page):
        if not obj:
            return None
        paginator = Paginator(obj, per_page=self.per_page)
        paginated_obj = paginator.page(page)
        return paginated_obj

    # if len(paginated_obj.object_list) > 1:
        # paginated_obj.object_list[0].is_first = True


class GetSingleTodoMixin:
    """
    To return an instance of TeamTodo, in the implementation add team_todo = True.
    To work, you need to pass the team in the url.
    """
    team_todo = False

    def get_object(self, *args, **kwargs):
        if not self.team_todo:
            return self.__get_user_todo()
        return self.__get_team_todo()

    def __get_user_todo(self):
        try:
            return UserTodo.objects.get(pk=self.kwargs['todo_pk'],
                                        title=self.kwargs['todo_title'],
                                        user=self.request.user)
        except (UserTodo.DoesNotExist, ValueError):
            return None

    def __get_team_todo(self):
        try:
            team = TeamJunction.objects.get(user=self.request.user, team__title=self.kwargs['team']).team
            return TeamTodo.objects.get(pk=self.kwargs['todo_pk'],
                                        title=self.kwargs['todo_title'],
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
