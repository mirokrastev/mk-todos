from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.views.generic import FormView
from accounts.models import CustomUser, UserProfile
from accounts.forms import (
    CustomPasswordChangeForm, CustomSetPasswordForm,
    UserProfileForm, CustomPasswordResetForm
)
from django.http import Http404
from utils.http import Http400
from accounts.mixins import GetUsernameMixin
from utils.mixins import GenericDispatchMixin, EnableSearchBarMixin
from django.urls import reverse_lazy
from accounts.common import upload_new_picture


class UserProfileView(GenericDispatchMixin, EnableSearchBarMixin, GetUsernameMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None
        self.profile = None
        self.is_trusted = None

    def dispatch(self, request, *args, **kwargs):
        username = self.get_username(kwargs)
        try:
            self.user = CustomUser.objects.get(username=username)
            self.profile = UserProfile.objects.get(user=self.user)
            self.is_trusted = self.request.user == self.user
        except (CustomUser.DoesNotExist, UserProfile.DoesNotExist):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['instance'] = self.alter_form(context['instance'])

        return render(self.request, 'accounts/user_profile.html', context)

    def post(self, request, *args, **kwargs):
        if not self.is_trusted:
            raise Http400

        new_picture = self.request.FILES.get('avatar', None)
        bio = self.request.POST.get('bio', None)

        if new_picture:
            upload_new_picture(self.profile, new_picture)

        if bio is not None:
            self.profile.bio = bio

        self.profile.save()

        return self.get(self.request, *args, **kwargs)

    def alter_form(self, instance):
        dd = {
            True: f'How do you feel today, {self.user.username} :)',
            False: f'{self.user.username} has no bio.',
        }

        if not self.is_trusted:
            for field in instance.fields.values():
                field.widget.attrs.update({'readonly': ""})

        if not self.profile.bio:
            instance.fields['bio'].widget.attrs.update({'placeholder': dd[self.is_trusted]})

        return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'username': self.user.username,
                        'profile': self.profile,
                        'instance': UserProfileForm(instance=self.profile),
                        'concrete': self.is_trusted})
        return context


class PasswordChange(GenericDispatchMixin, FormView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change/password_change.html'

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


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/reset/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/reset/password_reset_email.html'

    def form_valid(self, form):
        self.request.session['is_trusted'] = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = 'Submit'
        return context


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/reset/password_reset_done.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.session.pop('is_trusted', False) is False:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'accounts/reset/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

    def form_valid(self, form):
        self.request.session['is_trusted'] = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = 'Reset'
        return context


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/reset/password_reset_complete.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.session.pop('is_trusted', False) is False:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ChangeTheme(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'GET':
            raise Http400
        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        to_redirect = self.request.GET['next']
        user = UserProfile.objects.get(user=self.request.user)
        user.dark_mode = not user.dark_mode
        user.save()
        return redirect(to_redirect)
