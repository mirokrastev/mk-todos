from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({"placeholder": "Type your Task's name",
                                                  "class": "main_input"})
        self.fields['memo'].widget.attrs.update({"placeholder": "Type your memo",
                                                 "rows": 4})

    class Meta:
        model = Task
        fields = ['title', 'memo', 'important']
