from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login, logout
from accounts.models import CustomUser
from accounts.forms import LoginForm, CustomUserCreationForm
from django.http import Http404
from utils.http import Http400
from utils.mixins import GenericDispatchMixin
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from accounts.tokens import email_verification_token
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER
from smtplib import SMTPException


class RegisterView(GenericDispatchMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register/register.html'
    context_object_name = 'form'
    email_template_name = 'accounts/register/register_verification_email.html'
    title = 'Account activation | MK-TODOS'

    def form_valid(self, form):
        user = form.save(commit=False)
        email = form.cleaned_data['email']

        if not email:
            user.save()
            login(self.request, user)
            return render(self.request, 'home/home.html')

        user.is_active = False
        user.save()

        try:
            self.send_mail(user)
        except SMTPException:
            user.delete()
            context = {'admin_email': EMAIL_HOST_USER}
            return render(self.request, 'accounts/register/register_failed.html', context)

        return render(self.request, 'accounts/register/register_done.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = 'Sign Up'
        return context

    def send_mail(self, user):
        context = {
            'protocol': self.request.scheme,
            'domain': get_current_site(self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_verification_token.make_token(user),
            'username': user.username,
            'site_name': 'MK-TODOS',
        }

        message = render_to_string(self.email_template_name, context)
        send_mail(self.title, message, EMAIL_HOST_USER, (user.email,))


class ActivateAccountView(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'GET':
            raise Http400
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist, ValidationError):
            raise Http404

        if not email_verification_token.check_token(user, token):
            raise Http404

        user.is_active = True
        user.save()
        return render(self.request, 'accounts/register/register_complete.html')


class LoginView(GenericDispatchMixin, FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        credentials = {'username': form.cleaned_data['username'],
                       'password': form.cleaned_data['password']}

        user = authenticate(self.request, **credentials)

        if not user:
            context = self.get_context_data()
            form.add_error('password', 'Incorrect username or password!')
            context['form'] = form
            return self.render_to_response(context)

        login(self.request, user)
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = 'Log in'
        return context


class LogOutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http400
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        logout(self.request)
        return redirect('home')
