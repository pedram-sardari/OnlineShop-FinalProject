from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.db.models import Min, F, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, CreateView, ListView, DetailView, UpdateView, DeleteView

from products.forms import StoreProductForm, SelectProductForm, StoreDiscountForm
from products.models import StoreProduct, Category, StoreDiscount, Product
from website.mixins import IsStaffOfOwnerStore
from website.models import Address
from .forms import OwnerRegistrationForm, StaffRegistrationForm, StaffUpdateForm
from .models import Owner, Store, Staff


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

    @transaction.atomic
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


class StoreDiscountListView(ListView):
    model = StoreDiscount
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'store_discount_section': 'active'}
    context_object_name = 'store_discount_list'

    def get_queryset(self):
        owner = Owner.get_owner(user=self.request.user)
        return self.model.objects.filter(store=owner.store)


class StoreDiscountCreateView(CreateView):
    form_class = StoreDiscountForm
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'store_discount_section': 'active'}
    success_url = reverse_lazy('vendors:store-discount-list')

    def form_valid(self, form):
        store_discount = form.save(commit=False)
        owner = Owner.get_owner(user=self.request.user)
        store_discount.store = owner.store
        store_discount.save()
        response = super().form_valid(form)
        messages.success(self.request, f"StoreDiscountCreateView")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class StoreDiscountUpdateView(UpdateView):
    model = StoreDiscount
    form_class = StoreDiscountForm
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'store_discount_section': 'active'}
    success_url = reverse_lazy('vendors:store-discount-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"StoreDiscountUpdateView")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class StoreDiscountDeleteView(DeleteView):
    model = StoreDiscount
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'store_discount_section': 'active'}
    success_url = reverse_lazy('vendors:store-discount-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"StoreDiscountDeleteView")
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

    # todo 1
    # sort_by = {
    #     'best_seller': '-order_count',
    #     'highest_rating': '-product__rating_avg',
    #     'most_expensive': '-price',
    #     'cheapest': 'price'
    # }
    # ordering_kwargs = 'sort'
    # paginate_by = 0
    # paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # ordering = self.request.GET.get(self.ordering_kwargs) #todo 1
        # context['ordering'] = f"{self.ordering_kwargs}={ordering if ordering in self.sort_by else 'best_seller'}"
        context['dashboard_store_product_section'] = 'active'
        context['dashboard_store_product_list_section'] = True
        return context

    # def get_ordering(self): #todo 1
    #     return self.sort_by.get(self.request.GET.get(self.ordering_kwargs), '-order_count')

    def get_queryset(self):
        staff = Staff.get_staff(user=self.request.user)
        qs = self.model.objects.filter(
            store=staff.store
        ).annotate(
            order_count=Sum('order_items__quantity')
        ).order_by(
            'product__name'
        )
        return qs


class DashboardStoreProductDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ['products.view_storeproduct']
    template_name = 'vendors/dashboard/store_product_detail.html'
    context_object_name = 'staff'
    extra_context = {
        # 'staff_selected': 'active',
    }
    model = StoreProduct


class DashboardStoreProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['products.change_storeproduct']
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'dashboard_store_product_section': 'active',
    }
    model = StoreProduct
    form_class = StoreProductForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        owner = Owner.get_owner(user=self.request.user)
        kwargs['store'] = owner.store
        kwargs['product'] = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        return kwargs

    def get_success_url(self):
        return reverse_lazy('vendors:store-product-detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"DashboardStoreProductUpdateView")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class DashboardStoreProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['products.delete_storeproduct']
    model = StoreProduct
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'dashboard_store_product_section': 'active'}
    success_url = reverse_lazy('vendors:store-product-list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete(soft_delete=True)
        messages.success(self.request, f"DashboardStoreProductDeleteView")
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class SelectProductView(FormView):
    """To create a new `StoreProduct` you need to provide `Product` first. """
    template_name = 'accounts/dashboard/dashboard.html'
    form_class = SelectProductForm
    extra_context = {
        'dashboard_store_product_section': 'active',
        'create_new_product_link_section': True
    }

    def get_success_url(self):
        return reverse('vendors:store-product-create')

    def form_valid(self, form):
        product = form.cleaned_data.get('product')
        return redirect(reverse('vendors:store-product-create', kwargs={'product_id': product.id}))


class StoreProductsCreateView(CreateView):
    model = StoreProduct
    form_class = StoreProductForm
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'dashboard_store_product_section': 'active'}
    success_url = reverse_lazy('vendors:store-product-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        owner = Owner.get_owner(user=self.request.user)
        kwargs['store'] = owner.store
        kwargs['product'] = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        return kwargs

    def form_valid(self, form):
        store_product = form.save(commit=False)
        owner = Owner.get_owner(self.request.user)
        store_product.store = owner.store
        store_product.product = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        messages.success(self.request, f"StoreProductsCreateView")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class SelectCategoryListView(ListView):
    model = Category
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'dashboard_category_list_section': True}

    def get(self, request, *args, **kwargs):
        if category_slug := self.request.GET.get('category_slug'):
            category = get_object_or_404(self.model, slug=category_slug)
            if not self.model.objects.filter(parent_category=category).exists():
                return redirect(f"{reverse('vendors:store-product-create')}?category_slug={category.slug}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if category_slug := self.request.GET.get('category_slug'):
            return self.model.objects.filter(parent_category__slug=category_slug)
        return self.model.objects.filter(parent_category=None)
