from django.views import View
from django.contrib.auth.views import PasswordResetConfirmView
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import FormView
from accounts.mixins import GetUsernameMixin
from accounts.models import CustomUser, UserProfile
from accounts.forms import CustomPasswordChangeForm, CustomSetPasswordForm, UserProfileForm
from accounts.common import upload_new_picture


class UserProfileView(GetUsernameMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user: CustomUser = None
        self.username: str = None
        self.profile: UserProfile = None
        self.concrete: bool = None

    def dispatch(self, request, *args, **kwargs):
        self.username = self.get_username(kwargs)

        try:
            self.user = CustomUser.objects.get(username=self.username)
            self.profile = UserProfile.objects.get(user=self.user)
            self.concrete = self.request.user.username == self.username
        except (CustomUser.DoesNotExist, UserProfile.DoesNotExist):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print(self.request.method)
        context = self.get_context_data(inst=self.profile)
        context['instance'] = self.alter_form(context['instance'])

        return render(self.request, 'accounts/user_profile.html', context)

    def post(self, request, *args, **kwargs):
        if not self.concrete:
            raise Http404

        new_picture = request.FILES.get('avatar', None)
        bio = request.POST.get('bio', None)

        if new_picture:
            upload_new_picture(self.profile, new_picture)

        if bio is not None:
            self.profile.bio = bio

        self.profile.save()

        return self.get(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        inst = kwargs.get('inst', None)

        return {'username': self.username,
                'profile': self.profile, 'instance': UserProfileForm(instance=inst),
                'concrete': self.concrete}

    def alter_form(self, instance):
        dd = {
            True: f'How do you feel today, {self.username} :)',
            False: f'{self.username} has no bio.',
        }

        if not self.concrete:
            for field in instance.fields.values():
                field.widget.attrs.update({'readonly': ""})

        if not self.profile.bio:
            instance.fields['bio'].widget.attrs.update({'placeholder': dd[self.concrete]})

        return instance


class PasswordChange(FormView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        password = form.clean_new_password2()
        self.request.user.set_password(password)
        self.request.user.save()
        return redirect('home')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = 'Change'
        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = 'Reset'
        return context


def change_theme(request, previous_url):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user=request.user)
        user.dark_mode = not user.dark_mode
        user.save()
        return redirect(previous_url)
    raise Http404
