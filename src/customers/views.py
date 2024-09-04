from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.utils.translation import gettext_lazy as _

from accounts.forms import RegisterPhoneForm
from accounts.views import SendOTPView, VerifyOTPView
from orders.models import Order
from products.forms import CommentForm, RatingForm
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
        messages.success(self.request, _(f"Your account has been created successfully!"))
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
        'submit_button_content': _('Get Verification Code')
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


class OrderListView(PermissionRequiredMixin, ListView):
    permission_required = ['orders.view_order']
    model = Order
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'customer_dashboard__order_section': 'active',
        'order_list_section': True,
    }

    def get_queryset(self):
        customer = Customer.get_customer(user=self.request.user)
        qs = super().get_queryset(
        ).filter(
            customer=customer,
            is_paid=True
        ).order_by(
            "created_at"
        )
        return qs


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ['orders.view_order']
    model = Order
    template_name = 'accounts/dashboard/dashboard.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_dashboard__order_section'] = 'active'
        context['order_detail_section'] = True
        context['comment_form'] = CommentForm
        context['rating_form'] = RatingForm
        context['next_url'] = self.request.path
        return context
