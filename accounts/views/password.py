from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from accounts.forms import CustomSetPasswordForm, CustomPasswordResetForm
from django.http import Http404
from django.urls import reverse_lazy


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
