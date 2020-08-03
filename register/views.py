from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username, password = form.cleaned_data['username'], form.cleaned_data['password1']
            form = authenticate(request, username=username, password=password)
            login(request, form)
            return redirect('home')
    else:
        form = UserCreationForm()

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
    form = AuthenticationForm()

    return render(request, 'register/login.html', {'form': form, 'error': error})


def logout_view(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html', {'message': 'You are not logged in!'})

    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return render(request, 'home.html', {'message': 'Please use the Logout button'})
