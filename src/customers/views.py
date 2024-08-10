from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomerRegisterForm
from .models import Customer


class IsCustomerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_customer  # NOQA


class CustomerRegisterView(UserPassesTestMixin, CreateView):
    model = Customer
    template_name = 'accounts/register.html'
    form_class = CustomerRegisterForm
    success_url = reverse_lazy('accounts:login')
    extra_context = {'customer_register': 'active'}

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, 'شما با یک حساب کاربری در حال حاضر وارد شده اید')
        return redirect('home')

    def form_valid(self, form):
        messages.success(self.request, f"Your account has been created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)
