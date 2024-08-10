from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, DetailView, UpdateView, DeleteView

from website.models import Address
from .forms import OwnerRegistrationForm, StaffRegistrationForm, StaffUpdateForm
from .models import Owner, Store, Staff
from website.mixins import IsOwner, IsStaffOfOwnerStore


class OwnerRegisterView(UserPassesTestMixin, FormView):
    model = Owner
    template_name = 'accounts/register.html'
    form_class = OwnerRegistrationForm
    success_url = reverse_lazy('accounts:login')
    extra_context = {'staff_register': 'active'}

    def test_func(self):
        """A logged in must not be able to register"""
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, 'شما با یک حساب کاربری در حال حاضر وارد شده اید')
        return redirect('home')

    def form_valid(self, form):
        owner = form.save(commit=False)
        address = Address.objects.create(
            province=form.cleaned_data['province'],
            city=form.cleaned_data['city'],
            neighborhood=form.cleaned_data['neighborhood'],
            street=form.cleaned_data['street'],
            alley=form.cleaned_data['alley'],
            no=form.cleaned_data['no'],
            zipcode=form.cleaned_data['zipcode']
        )
        store = Store.objects.create(
            name=form.cleaned_data['store_name'],
            address=address
        )
        owner.store = store
        owner.save()
        messages.success(self.request, f"Your account has been created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class StaffRegisterView(LoginRequiredMixin, IsOwner, CreateView):
    model = Staff
    template_name = 'accounts/dashboard/dashboard.html'
    form_class = StaffRegistrationForm
    success_url = reverse_lazy('vendors:staff-list')
    extra_context = {
        'stor_info': 'active',
        'form_section': 'active'
    }

    def form_valid(self, form):
        staff = form.save(commit=False)
        owner = Owner.get_owner(self.request.user)
        staff.store = owner.store
        staff.save()
        response = super().form_valid(form)
        messages.success(self.request, f"RegisterManagerView")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class StaffListView(LoginRequiredMixin, IsOwner, ListView):
    template_name = 'accounts/dashboard/dashboard.html'
    context_object_name = 'staff_list'
    extra_context = {
        'staff_selected': 'active',
    }
    success_url = reverse_lazy('accounts:user-address-list')

    def get_queryset(self):
        owner = Owner.get_owner(user=self.request.user)
        return owner.store.staffs.exclude(id=owner.id)


class StaffDetailView(LoginRequiredMixin, IsStaffOfOwnerStore, DetailView):
    template_name = 'accounts/dashboard/dashboard.html'
    context_object_name = 'staff'
    extra_context = {
        'staff_selected': 'active',
    }
    model = Staff


class StaffUpdateView(LoginRequiredMixin, IsStaffOfOwnerStore, UpdateView):
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'staff_selected': 'active',
        'form_section': 'active'
    }
    model = Staff
    form_class = StaffUpdateForm

    def get_success_url(self):
        return reverse_lazy('vendors:staff-detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"StaffUpdateView")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class StaffDeleteView(LoginRequiredMixin, IsStaffOfOwnerStore, DeleteView):
    template_name = 'accounts/dashboard/dashboard.html'
    model = Staff
    success_url = reverse_lazy('vendors:staff-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"StaffUpdateView")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)
