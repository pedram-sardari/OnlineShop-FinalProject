from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url, redirect
from django.contrib.auth.views import LoginView, LogoutView, RedirectURLMixin
from django.views import View
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DetailView, DeleteView, FormView

from django.conf import settings
from website.mixins import IsAddressForLoggedInUser
from .forms import LoginForm, MyUserChangeForm, UserAddressForm, PhoneForm, VerificationCodeForm
from django.urls import reverse_lazy
from django.shortcuts import reverse

from .models import UserAddress, User
from .utils import generate_otp, send_otp


class EmailLoginView(LoginView):
    template_name = 'accounts/login_email.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        return reverse('accounts:personal-info-detail')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome dear '{str(self.request.user)}'")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class PhoneLoginView(FormView):
    template_name = 'accounts/login_phone.html'
    form_class = PhoneForm
    success_url = reverse_lazy('accounts:login-phone-verify')
    extra_context = {'get_code_button': True}

    def form_valid(self, form):
        phone = form.cleaned_data.get('phone')
        otp = generate_otp()
        self.request.session['phone'] = phone
        self.request.session['otp'] = otp
        self.request.session.set_expiry(settings.OTP_EXPIRATION_TIME)
        send_otp(otp, phone)
        return redirect(self.success_url)


class PhoneLoginVerifyView(FormView):
    template_name = 'accounts/login_phone.html'
    form_class = VerificationCodeForm
    success_url = reverse_lazy('home')
    extra_context = {'login_button': True}

    def form_valid(self, form):
        user_otp = form.cleaned_data.get('verification_code')
        session_otp = self.request.session.get('otp')
        print('=' * 50, user_otp, session_otp)
        if not session_otp:
            messages.error(self.request, 'کد تایید منقضی شده است')
            return redirect('accounts:login-phone')
        elif user_otp == session_otp:
            try:
                user = User.objects.get(phone=self.request.session.get('phone'))
                messages.success(self.request,
                                 f"Your are successfully logged in with `{self.request.session['phone']}`")
                del self.request.session['otp']
                self.request.session.delete()
                login(self.request, user)
                return super().form_valid(form)
            except User.DoesNotExist:
                messages.error(self.request, f"شما ثبتنام نکرده اید")
        else:
            messages.error(self.request, f"کد تایید اشتباه است")
        return super().form_invalid(form)


class MyLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('home')


class PersonalInfoDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'personal_info_detail': 'active'}


class PersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'personal_info_update': 'active',
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
