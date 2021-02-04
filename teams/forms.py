from django import forms
from teams.models import Team
from django.core.validators import MinLengthValidator


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {"placeholder": "Enter Team name",
             "class": "main_input"}
        )
        self.fields['title'].validators = [MinLengthValidator(2)]

    class Meta:
        model = Team
        fields = ('title',)


class TeamIdentifierForm(forms.Form):
    identifier = forms.CharField(max_length=20, required=True,
                                 validators=[MinLengthValidator(6)],
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'Type the Team\'s identifier',
                                            'class': 'main_input'})
                                 )
