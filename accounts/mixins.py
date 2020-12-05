class GetUsernameMixin:
    def get_username(self, kwargs):
        query_name = self.request.GET.get('q', None)
        url_name = kwargs.get('username', None)
        return query_name if query_name else url_name
