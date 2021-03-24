from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.views.generic.base import ContextMixin
from django.contrib.auth import logout
from accounts.models import CustomUser, UserProfile
from accounts.forms import CustomPasswordChangeForm, UserProfileForm
from django.http import Http404
from utils.http import Http400
from utils.mixins import GenericDispatchMixin, EnableSearchBarMixin
from django.urls import reverse_lazy
from accounts.common import upload_new_picture


class UserProfileView(GenericDispatchMixin, EnableSearchBarMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None
        self.profile = None
        self.is_trusted = None

    def dispatch(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            username = self.request.GET['q']
            return redirect(reverse_lazy('accounts:my_profile', kwargs={'username': username}))

        username = self.kwargs['username']
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


class DeleteProfileView(GenericDispatchMixin, ContextMixin, View):
    def get(self, request):
        context = self.get_context_data()
        return render(self.request, 'accounts/delete/profile_delete.html', context)

    def post(self, request):
        user = CustomUser.objects.get(username=self.request.user.username)
        logout(self.request)
        user.delete()
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = 'Delete'
        return context


class ChangeTheme(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http400
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        to_redirect = self.request.META['HTTP_REFERER']
        userprofile = UserProfile.objects.get(user=self.request.user)
        userprofile.dark_mode = not userprofile.dark_mode
        userprofile.save()
        return redirect(to_redirect)
