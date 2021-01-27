from django.core.paginator import Paginator
from django.http import Http404
from teams.models import TeamJunction
from todolist.models import UserTodo, TeamTodo


class GetRequestsMixin:
    ORDER_BY = {'oldest': 'date_created', 'newest': '-date_created'}

    def make_query_params(self):
        page = self.request.GET.get('page', 1)
        order = self.ORDER_BY[self.request.GET.get('order_by', 'newest')]
        word = self.request.GET.get('q', None)

        return page, order, word


class PaginateObjectMixin:
    def paginate(self, obj, page):
        if not obj:
            return None
        paginator = Paginator(obj, per_page=4)
        paginated_obj = paginator.page(page)
        if len(paginated_obj.object_list) > 1:
            paginated_obj.object_list[0].is_first = True
        return paginated_obj


class FilterTodosMixin:
    def filter_todos(self, order, word, is_null=True):
        if not self.request.user.is_authenticated:
            return None

        params = {'date_completed__isnull': is_null}
        if word:
            params.update({'title__icontains': word})

        user_todos = UserTodo.objects.filter(user=self.request.user, **params).order_by(order)
        return user_todos
        # TODO: IMPLEMENT TEAM TODOS, IMPLEMENT WITH CACHE SYSTEM FOR FASTER READ!
        # user_teams = TeamJunction.objects.filter(user=self.request.user)
        # user_team_todos = [todo
        #                  for query in user_teams
        #                  for todo in TeamTodo.objects.filter(team=query.team)]


class GetSingleTodoMixin:
    def get_object(self):
        try:
            return UserTodo.objects.get(pk=self.kwargs['task_pk'], user=self.request.user)
        except (UserTodo.DoesNotExist, ValueError):
            return None


class InitializeTodoMixin(GetSingleTodoMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = None

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        if not self.request.method == 'POST' or not self.task:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
