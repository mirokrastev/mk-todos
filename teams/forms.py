from django import forms
from teams.models import Team
from django.core.exceptions import ValidationError


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {"placeholder": "Enter Team name",
             "class": "main_input"}
        )

    def clean_title(self):
        title = self.cleaned_data['title']
        if Team.objects.get_or_none(title=title):
            raise ValidationError('Team with this name already exists!')

    class Meta:
        model = Team
        fields = ('title',)


class TeamIdentifierForm(forms.Form):
    identifier = forms.CharField(max_length=20, required=True,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'Type the Team\'s identifier',
                                            'class': 'main_input'})
                                 )
