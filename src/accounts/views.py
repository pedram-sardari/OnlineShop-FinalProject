from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DetailView, DeleteView

from customers.models import Customer
from orders.utils import sync_session_and_db_carts
from website.mixins import IsAddressForLoggedInUser, CustomRedirectURLMixin, DjangoLoginDispatchMixin
from .forms import LoginForm, MyUserChangeForm, UserAddressForm, LoginPhoneForm, EmailAndPasswordChangeForm
from .models import UserAddress, User
from .views_base import SendOTPView, VerifyOTPView


class EmailLoginView(CustomRedirectURLMixin, LoginView):
    template_name = 'accounts/login_email.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        if customer := Customer.get_customer(user=form.get_user()):
            sync_session_and_db_carts(self.request, customer)
        messages.success(self.request, f"Welcome dear '{str(self.request.user)}'")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class PhoneLoginView(DjangoLoginDispatchMixin, SendOTPView):
    template_name = 'accounts/login_phone.html'
    form_class = LoginPhoneForm
    success_url = reverse_lazy('accounts:login-phone-verify')
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_success_url(self):
        # pass the `next` query param to the `PhoneLoginVerifyView`
        next_url = self.request.GET.get(self.redirect_field_name)
        next_param = f"?{self.redirect_field_name}={next_url}" if next_url else ''
        return f"{str(self.success_url)}{next_param}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_otp_button'] = True
        context[self.redirect_field_name] = self.request.GET.get(self.redirect_field_name)
        return context


class PhoneLoginVerifyView(DjangoLoginDispatchMixin, CustomRedirectURLMixin, VerifyOTPView):
    template_name = 'accounts/login_phone.html'
    model = User
    success_url = reverse_lazy('home')
    failed_url = reverse_lazy('accounts:login-phone')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_button'] = True
        context[self.redirect_field_name] = self.get_redirect_url()
        return context


class MyLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('home')


class PersonalInfoDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'personal_info_detail': 'active',
        'account_info': 'active',
    }


class PersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'personal_info_update': 'active',
        'account_info': 'active',
        'form_section': 'active'
    }
    form_class = MyUserChangeForm
    success_url = reverse_lazy('accounts:personal-info-detail')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"PersonalInfoUpdateView")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class EmailAndPasswordDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'email_and_password_detail': 'active',
        'account_info': 'active',
    }


class EmailAndPasswordUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'email_and_password_update': 'active',
        'account_info': 'active',
        'form_section': 'active'
    }
    form_class = EmailAndPasswordChangeForm
    success_url = reverse_lazy('accounts:email-and-password-detail')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        kwargs.pop('instance', None) # instance is an extra argument
        user = self.get_object()
        return self.form_class(user, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"PersonalInfoUpdateView")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class UserAddressListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'user_address_list': 'active'}
    success_url = reverse_lazy('accounts:user-address-list')

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class UserAddressCreateView(LoginRequiredMixin, CreateView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'user_address_create': 'active',
        'form_section': 'active'
    }
    model = UserAddress
    form_class = UserAddressForm
    success_url = reverse_lazy('accounts:user-address-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, f"UserAddressCreateView")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class UserAddressDetailView(LoginRequiredMixin, IsAddressForLoggedInUser, DetailView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'user_address_detail': 'active',
    }
    context_object_name = 'user_address'
    model = UserAddress


class UserAddressUpdateView(LoginRequiredMixin, IsAddressForLoggedInUser, UpdateView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'user_address_update': 'active',
        'form_section': 'active'
    }
    model = UserAddress
    form_class = UserAddressForm

    def get_success_url(self):
        return reverse_lazy('accounts:user-address-detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"PersonalInfoUpdateView")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class UserAddressDeleteView(LoginRequiredMixin, IsAddressForLoggedInUser, DeleteView):
    template_name = 'accounts/dashboard/dashboard.html'
    model = UserAddress
    success_url = reverse_lazy('accounts:user-address-list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete(soft_delete=True)
        messages.success(self.request, f"PersonalInfoUpdateView")
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)
