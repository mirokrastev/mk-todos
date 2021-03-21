from utils.http import Http400
from django.views.generic.base import ContextMixin
from django.core.paginator import Paginator


class GenericDispatchMixin:
    """
    Mixin to check if request's method is either GET or POST.
    If not, raise Http400 Suspicious Operation.
    """
    def dispatch(self, request, *args, **kwargs):
        if self.request.method not in ('GET', 'POST'):
            raise Http400
        return super().dispatch(request, *args, **kwargs)


class EnableSearchBarMixin(ContextMixin):
    """
    Simple Mixin to make it easier to enable the search bar for authenticated users.
    It's just adding one key-value pair in the context and returning it.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'enable_search': True})
        return context


class PaginateObjectMixin:
    """
    Mixin that paginate objects. You need to specify per_page (orphans is optional).

    You can customize it even further by specifying per_page and orphans (optional) in the
    paginate method.
    """
    per_page = None
    orphans = 0

    def paginate(self, obj, page, per_page=None, orphans=None):
        self.per_page = per_page or self.per_page
        self.orphans = orphans or self.orphans

        paginator = Paginator(obj, per_page=self.per_page, orphans=self.orphans)
        paginated_obj = paginator.page(page)
        return paginated_obj

    # if len(paginated_obj.object_list) > 1:
    # paginated_obj.object_list[0].is_first = True
