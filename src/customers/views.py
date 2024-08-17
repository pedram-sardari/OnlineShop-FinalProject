from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from accounts.forms import RegisterPhoneForm
from accounts.views import SendOTPView, VerifyOTPView
from products.models import Comment
from website.mixins import IsNotAuthenticated
from .forms import CustomerRegisterForm
from .models import Customer, User


class CustomerRegisterByEmailView(IsNotAuthenticated, CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomerRegisterForm
    success_url = reverse_lazy('accounts:personal-info-detail')
    extra_context = {
        'customer_register': 'active',
        'by_phone_link': reverse_lazy('customers:register-by-phone'),
        'by_email_link': reverse_lazy('customers:register-by-email'),
        'by_email': 'active'
    }

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.save()
        user = User.objects.get(id=customer.id)
        self.request.session.flush()
        login(self.request, user)
        messages.success(self.request, f"Your account has been created successfully!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class CustomerRegisterByPhoneView(IsNotAuthenticated, SendOTPView):
    template_name = 'accounts/register.html'
    form_class = RegisterPhoneForm
    success_url = reverse_lazy('customers:register-by-phone-verify')
    extra_context = {
        'customer_register': 'active',
        'by_email_link': reverse_lazy('customers:register-by-email'),
        'by_phone_link': reverse_lazy('customers:register-by-phone'),
        'by_phone': 'active',
        'submit_button_content': 'دریافت کد تائید'
    }


class CustomerRegisterByPhoneVerifyView(IsNotAuthenticated, VerifyOTPView):
    template_name = 'accounts/register.html'
    model = Customer
    success_url = reverse_lazy('accounts:personal-info-detail')
    failed_url = reverse_lazy('accounts:login-phone')
    extra_context = {
        'customer_register': 'active',
        'by_email_link': reverse_lazy('customers:register-by-email'),
        'by_phone_link': reverse_lazy('customers:register-by-phone'),
        'by_phone': 'active',
    }


class MyCommentsListView(PermissionRequiredMixin, ListView):
    permission_required = ['products.view_comment']
    model = Comment
    template_name = 'accounts/dashboard/dashboard.html'
    context_object_name = 'comment_list'
    extra_context = {
        'my_comment_list_section': True,
    }

    def get_queryset(self):
        return Comment.objects.filter(customer=Customer.get_customer(self.request.user))
