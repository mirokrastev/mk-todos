from django.core.paginator import Paginator


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
