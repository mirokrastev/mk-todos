from todolist.models import Task
from todolist.views.todo_creation.abstract import AbstractMakeTodos


class MakeGenericTodos(AbstractMakeTodos):
    def make_todos(self, order, is_null=True):
        todos = Task.objects.filter(user=self.request.user, date_completed__isnull=is_null).order_by(order)
        return todos


class MakeSearchTodos(AbstractMakeTodos):
    def make_todos(self, order, word):
        todos = Task.objects.filter(user=self.request.user, title__icontains=word).order_by(order)
        return todos
