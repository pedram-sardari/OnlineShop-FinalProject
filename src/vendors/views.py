from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, DetailView, UpdateView, DeleteView

from website.models import Address
from .forms import OwnerRegistrationForm, StaffRegistrationForm, StaffUpdateForm
from .models import Owner, Store, Staff
from website.mixins import IsStaffOfOwnerStore


class OwnerRegisterView(UserPassesTestMixin, FormView):
    model = Owner
    template_name = 'accounts/register.html'
    form_class = OwnerRegistrationForm
    success_url = reverse_lazy('accounts:login-email')
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


class StaffRegisterView(PermissionRequiredMixin, CreateView):
    permission_required = ['vendors.add_staff']
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


class StaffListView(PermissionRequiredMixin, ListView):
    permission_required = ['vendors.view_staff']
    template_name = 'accounts/dashboard/dashboard.html'
    context_object_name = 'staff_list'
    extra_context = {
        'staff_selected': 'active',
    }
    success_url = reverse_lazy('accounts:user-address-list')

    def get_queryset(self):
        owner = Owner.get_owner(user=self.request.user)
        return owner.store.staffs.exclude(id=owner.id)


class StaffDetailView(PermissionRequiredMixin, IsStaffOfOwnerStore, DetailView):
    permission_required = ['vendors.view_staff']
    template_name = 'accounts/dashboard/dashboard.html'
    context_object_name = 'staff'
    extra_context = {
        'staff_selected': 'active',
    }
    model = Staff


class StaffUpdateView(PermissionRequiredMixin, IsStaffOfOwnerStore, UpdateView):
    permission_required = ['vendors.change_staff']
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


class StaffDeleteView(PermissionRequiredMixin, IsStaffOfOwnerStore, DeleteView):
    permission_required = ['vendors.delete_staff']
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


class DashboardStoreProductListView(PermissionRequiredMixin, ListView):
    permission_required = ['products.view_storeproduct']
    model = StoreProduct
    template_name = 'accounts/dashboard/dashboard.html'
    context_object_name = 'store_product_list'
    sort_by = {
        'best_seller': '-order_count',
        'highest_rating': '-product__rating_avg',
        'most_expensive': '-price',
        'cheapest': 'price'
    }
    ordering_kwargs = 'sort'
    paginate_by = 3
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        ordering = self.request.GET.get(self.ordering_kwargs)
        context['ordering'] = f"{self.ordering_kwargs}={ordering if ordering in self.sort_by else 'best_seller'}"
        context['dashboard_store_product_section'] = True
        return context

    def get_ordering(self):
        return self.sort_by.get(self.request.GET.get(self.ordering_kwargs), '-order_count')

    def get_queryset(self):
        staff = Staff.get_staff(user=self.request.user)
        qs = self.model.objects.filter(
            store=staff.store
        ).filter(
            inventory__gt=0
        ).annotate(
            min_price=Min('product__store_products__price')
        ).filter(
            price=F('min_price')
        ).annotate(
            order_count=Sum('order_items__quantity')
        ).order_by(
            self.get_ordering()
        ).distinct()
        print('2' * 50)
        print(repr(qs.values('order_count')))
        print('1' * 50)
        return qs


