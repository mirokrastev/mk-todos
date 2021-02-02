from django.views import View
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.urls import reverse
from abc import ABC, abstractmethod
from utils.http import Http400


class BaseRedirectFormView(ABC, FormMixin, View):
    """
    Base Redirect Form View for handling the form and form errors.
    You should supply form_class, success_url (class attributes) and give an interface to the form_valid method.

    The main difference between this class and FormView is,
    that this class works with sessions and redirects,
    where FormView renders the same page with form's errors.
    """
    post_only = True

    def dispatch(self, request, *args, **kwargs):
        if self.post_only and not self.request.method == 'POST':
            raise Http400
        self.request.session['errors'] = []
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if not form.is_valid():
            return self.form_invalid(*form.errors.values())
        return self.form_valid(form)

    @abstractmethod
    def form_valid(self, form):
        pass

    def form_invalid(self, errors=None):
        errors = errors or []
        self.request.session['errors'].extend(errors)
        return self.redirect()

    def redirect(self, redirect_kwargs=None):
        redirect_kwargs = redirect_kwargs or {}
        return redirect(reverse(self.get_success_url(), kwargs={**redirect_kwargs}))
