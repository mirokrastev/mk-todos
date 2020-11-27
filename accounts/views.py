import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login, logout, authenticate
from django.views import View
from django.views.generic import CreateView, FormView
from .models import UserProfile, CustomUser
from .forms import CustomUserCreationForm, CustomSetPasswordForm, CustomPasswordChangeForm, UserProfileForm
from django.http import Http404


def delete_image(path):
    if not os.path.exists(path):
        return
    os.remove(path)


def upload_new_picture(profile, new_picture):
    old_picture = profile.avatar.name.split('/')[-1]
    if old_picture != 'default-user-avatar.jpg':
        delete_image(profile.avatar.path)
    profile.avatar = new_picture


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button_value'] = 'Sign Up'
        return context

    def form_valid(self, form):
        form = form.save()
        UserProfile.objects.create(user=form)
        login(self.request, form)
        return redirect('home')


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


class LogOutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        logout(self.request)
        return redirect('home')


class UserProfileView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None
        self.profile = None
        self.concrete = None

    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        try:
            self.user = CustomUser.objects.get(username=username)
            self.profile = UserProfile.objects.get(user=self.user)
            self.concrete = self.request.user.username == username
        except (CustomUser.DoesNotExist, UserProfile.DoesNotExist):
            return Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        context = self.get_context_data(username=username, inst=self.profile)
        context['instance'] = self.alter_form(context)

        return render(self.request, 'accounts/user_profile.html', context)

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        if not self.request.user.username == username:
            raise Http404

        new_picture = request.FILES.get('avatar', None)
        bio = request.POST.get('bio', None)

        if new_picture:
            upload_new_picture(self.profile, new_picture)

        if bio is not None:
            self.profile.bio = bio

        self.profile.save()

        return self.get(self.request, username, *args, **kwargs)

    def get_context_data(self, **kwargs):
        (username, inst) = (kwargs.get('username', None), kwargs.get('inst', None))

        return {'username': username,
                'profile': self.profile, 'instance': UserProfileForm(instance=inst),
                'concrete': self.concrete}

    def alter_form(self, context):
        (instance, username) = (context['instance'], context['username'])

        dd = {
            True: f'How do you feel today, {username} :)',
            False: f'{username} has no bio.',
        }

        if not self.concrete:
            for field in instance.fields.values():
                field.widget.attrs.update({'readonly': ""})

        if not self.profile.bio:
            instance.fields['bio'].widget.attrs.update({'placeholder': dd[self.concrete]})

        return instance


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
