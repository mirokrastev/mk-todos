from django import forms
from todolist.models import UserTodo, TeamTodo


class TodoFormWidgetMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {"placeholder": "Type your Todo name",
             "class": "main_input"}
        )

        self.fields['title'].label = ''

        self.fields['memo'].widget.attrs.update(
            {"placeholder": "Type your memo",
             "class": "transparent",
             "rows": 5, "cols": 30}
        )

        self.fields['memo'].label = ''


class UserTodoForm(TodoFormWidgetMixin, forms.ModelForm):
    class Meta:
        model = UserTodo
        fields = ('title', 'memo', 'important')


class TeamTodoForm(TodoFormWidgetMixin, forms.ModelForm):
    class Meta:
        model = TeamTodo
        fields = ('title', 'memo', 'important', 'team')
