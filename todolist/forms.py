from django import forms
from .models import UserTodo


class TodoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {"placeholder": "Type your Todo name",
             "class": "main_input"}
        )

        self.fields['memo'].widget.attrs.update(
            {"placeholder": "Type your memo",
             "class": "transparent",
             "rows": 5, "cols": 30}
        )

    class Meta:
        model = UserTodo
        fields = ('title', 'memo', 'important')
        labels = {
            'title': '',
            'memo': '',
        }
