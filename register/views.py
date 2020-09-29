from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.http import Http404


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username, password = form.cleaned_data['username'], form.cleaned_data['password1']
            form = authenticate(request, username=username, password=password)
            login(request, form)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register/register.html', {'form': form})


def login_view(request):
    error = None
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        form = authenticate(request, username=username, password=password)

        if form:
            login(request, form)
            return redirect('home')

        error = 'Incorrect username or password! Please try again!'

    return render(request, 'register/login.html', {'error': error})


@login_required
def logout_view(request):
    if not request.method == 'POST':
        return Http404

    logout(request)
    return redirect('home')
