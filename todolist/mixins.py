from django.core.paginator import Paginator
from django.http import Http404
from todolist.models import Task


class GetRequestMixin:
    def make_query_params(self):
        page = self.request.GET.get('page', 1)
        order = self.__class__.ORDER_BY[self.request.GET.get('order_by', 'newest')]
        word = self.request.GET.get('q', None)

        return page, order, word


class PaginatePageMixin:
    def paginate(self, todos, page):
        if not todos:
            return None
        paginator = Paginator(todos, 6)
        todos = paginator.page(page)
        todos.object_list[0].is_first = True
        return todos


class GetTodoMixin:
    def get_object(self):
        try:
            return Task.objects.get(pk=self.kwargs['task_pk'], user=self.request.user)
        except (Task.DoesNotExist, ValueError):
            return None


class MakeGenericTodoMixin(GetTodoMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = None

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        if not self.request.method == 'POST' or not self.task:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
