from todolist.models import Task
from todolist.views.todo_creation.abstract import AbstractMakeTodos


class MakeGenericTodos(AbstractMakeTodos):
    def make_todos(self, order, word, is_null=True):
        params = {'date_completed__isnull': is_null}
        if word:
            params.update({'title__icontains': word})

        todos = Task.objects.filter(user=self.request.user, **params).order_by(order)
        return todos
