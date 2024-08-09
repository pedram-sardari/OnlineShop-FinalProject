from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, FormView, UpdateView

from .models import Customer
from .forms import CustomerRegisterForm,   CustomerChangeForm


class CustomerRegisterView(UserPassesTestMixin, CreateView):
    model = Customer
    template_name = 'accounts/register.html'
    form_class = CustomerRegisterForm
    success_url = reverse_lazy('login')
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


class PersonalInfoDisplayView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'customers/dashboard.html'
    extra_context = {'personal_info_display': 'active'}

    def test_func(self):
        return self.request.user.is_customer


class PersonalInfoEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'customers/dashboard.html'
    extra_context = {'personal_info_edit': 'active'}
    form_class = CustomerChangeForm
    success_url = reverse_lazy('customers:personal-info-display')

    def get_object(self, queryset=None):
        return Customer.objects.get(id=self.request.user.id)

    def test_func(self):
        return self.request.user.is_customer

