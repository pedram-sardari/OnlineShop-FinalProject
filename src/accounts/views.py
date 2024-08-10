from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DetailView, DeleteView

from website.mixins import IsAddressForLoggedInUser
from .forms import LoginForm, MyUserChangeForm, UserAddressForm
from django.urls import reverse_lazy
from django.shortcuts import reverse

from .models import UserAddress


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
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
