from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CustomSetPasswordForm, CustomPasswordChangeForm
from django.http import Http404


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username, password = form.cleaned_data['username'], form.cleaned_data['password1']
            form = authenticate(request, username=username, password=password)
            login(request, form)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'button_value': 'Sign Up'}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    error = None
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        form = authenticate(request, username=username, password=password)

        if form:
            login(request, form)
            return redirect('home')

        error = 'Incorrect username or password! Please try again!'

    return render(request, 'accounts/login.html', {'error': error})


@login_required
def logout_view(request):
    if not request.method == 'POST':
        return Http404

    logout(request)
    return redirect('home')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            password = request.POST['new_password1']
            request.user.set_password(password)
            request.user.save()
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {'form': form, 'button_value': 'Change'}
    return render(request, 'accounts/register.html', context)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_context = {'button_value': 'Reset'}
