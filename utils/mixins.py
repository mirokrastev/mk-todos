from utils.http import Http400
from django.views.generic.base import ContextMixin


class GenericDispatchMixin:
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
