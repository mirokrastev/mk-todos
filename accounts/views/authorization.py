from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import CreateView, FormView
from accounts.forms import LoginForm, CustomUserCreationForm
from accounts.models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_value'] = 'Sign Up'
        return context

    def form_valid(self, form):
        form = form.save()
        login(self.request, form)
        return redirect('home')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        credentials = {'username': form.cleaned_data['username'],
                       'password': form.cleaned_data['password']}

        user = authenticate(self.request, **credentials)

        if not user:
            context = self.get_context_data()
            context['error'] = 'Incorrect username or password!'
            return self.render_to_response(context)

        login(self.request, user)
        return redirect('home')


class LogOutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        logout(self.request)
        return redirect('home')


class DeleteProfileView(View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.method not in ('GET', 'POST'):
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(self.request, 'accounts/delete/profile_delete.html')

    def post(self, request):
        user = CustomUser.objects.get(username=self.request.user.username)
        logout(self.request)
        user.delete()
        return redirect('home')
