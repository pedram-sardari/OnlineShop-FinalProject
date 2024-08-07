from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.urls import reverse_lazy
from django.shortcuts import reverse


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        if self.request.user.is_customer:
            return reverse('customer-panel')
        return reverse('vendor-panel')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome dear '{str(self.request.user)}'")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class MyLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('home')
