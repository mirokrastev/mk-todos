class GetRequestMixin:
    def make_query_params(self):
        page = self.request.GET.get('page', 1)
        order = self.__class__.ORDER_BY[self.request.GET.get('order_by', 'newest')]
        word = self.request.GET.get('q', None)

        return page, order, word
