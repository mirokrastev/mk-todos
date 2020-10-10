from django.contrib.auth import forms as auth_forms
from django import forms
from .models import CustomUser


class CustomUserCreationForm(auth_forms.UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter your email address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'username',
                                                     'class': 'main_input'})

        self.fields['password1'].widget.attrs.update({'placeholder': 'password',
                                                      'class': 'main_input'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'retype password',
                                                      'class': 'main_input'})

        self.fields['email'].widget.attrs.update({'placeholder': 'email',
                                                  'class': 'main_input'})

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email',
                                                  'class': 'main_input'})


class CustomSetPasswordForm(auth_forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'Enter your password',
                                                          'class': 'main_input'})

        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Retype your password',
                                                          'class': 'main_input'})

        self.fields['new_password2'].help_text = 'Retype your password'


class CustomPasswordChangeForm(CustomSetPasswordForm, auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({'placeholder': 'Enter your old password',
                                                         'class': 'main_input',
                                                         'autocomplete': 'new-password'})
        self.fields['old_password'].help_text = 'Enter your old password'
