from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomerEmailRegisterForm
from .models import Customer, User


class CustomerRegisterView(UserPassesTestMixin, CreateView):
    model = Customer
    template_name = 'accounts/register.html'
    form_class = CustomerEmailRegisterForm
    success_url = reverse_lazy('accounts:personal-info-detail')
    extra_context = {'customer_register': 'active'}

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, 'شما با یک حساب کاربری در حال حاضر وارد شده اید')
        return redirect('home')

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.save()
        user = User.objects.get(id=customer.id)
        login(self.request, user)
        messages.success(self.request, f"Your account has been created successfully!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)
