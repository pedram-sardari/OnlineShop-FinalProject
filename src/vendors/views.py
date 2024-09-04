from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.db.models import Sum
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from accounts.forms import RegisterPhoneForm
from accounts.views_base import SendOTPView, VerifyOTPView
from orders.models import OrderItem
from products.forms import StoreProductForm, SelectProductForm, StoreDiscountForm
from products.models import StoreProduct, Category, StoreDiscount, Product, ProductImage
from website.mixins import IsStaffOfOwnerStore, IsNotAuthenticated
from .forms import (OwnerRegisterEmailForm, StaffRegistrationForm, StaffUpdateForm, StoreForm,
                    OrderItemStatusUpdateForm, ProductForm)
from .models import Owner, Store, Staff


class OwnerRegisterByEmailView(IsNotAuthenticated, FormView):
    template_name = 'accounts/register.html'
    form_class = OwnerRegisterEmailForm
    success_url = reverse_lazy('vendors:store-create')
    extra_context = {
        'owner_register': 'active',
        'by_phone_link': reverse_lazy('vendors:register-owner-by-phone'),
        'by_email_link': reverse_lazy('vendors:register-owner-by-email'),
        'by_email': 'active',
        'submit_button_content': _('Continue')
    }

    def form_valid(self, form):
        self.request.session['email'] = form.cleaned_data.get('email')
        self.request.session['hashed_password'] = make_password(form.cleaned_data.get('password2'))
        self.request.session.set_expiry(settings.OWNER_REGISTRATION_TIMEOUT)
        response = redirect(self.success_url)
        response.set_cookie('sessionid', self.request.session.session_key)
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class OwnerRegisterByPhoneView(IsNotAuthenticated, SendOTPView):
    template_name = 'accounts/register.html'
    form_class = RegisterPhoneForm
    success_url = reverse_lazy('vendors:register-owner-by-phone-verify')
    extra_context = {
        'owner_register': 'active',
        'by_email_link': reverse_lazy('vendors:register-owner-by-email'),
        'by_phone_link': reverse_lazy('vendors:register-owner-by-phone'),
        'by_phone': 'active',
        'submit_button_content': _('Get verification code')
    }


class OwnerRegisterByPhoneVerifyView(IsNotAuthenticated, VerifyOTPView):
    template_name = 'accounts/register.html'
    model = Owner
    success_url = reverse_lazy('vendors:store-create')
    failed_url = reverse_lazy('accounts:login-phone')
    extra_context = {
        'owner_register': 'active',
        'by_email_link': reverse_lazy('vendors:register-owner-by-email'),
        'by_phone_link': reverse_lazy('vendors:register-owner-by-phone'),
        'by_phone': 'active',
        'submit_button_content': _('continue')
    }

    def form_valid(self, form):
        self.request.session.pop('otp')
        self.request.session.set_expiry(settings.OWNER_REGISTRATION_TIMEOUT)
        response = redirect(self.success_url)
        response.set_cookie('sessionid', self.request.session.session_key)
        return response


class StoreCreateView(UserPassesTestMixin, FormView):
    template_name = 'accounts/register.html'
    form_class = StoreForm
    success_url = reverse_lazy('accounts:personal-info-detail')
    extra_context = {
        'owner_register': 'active',
        'by_email_link': reverse_lazy('vendors:register-owner-by-email'),
        'by_email': 'active',
    }

    def test_func(self):
        phone = self.request.session.get('phone')
        email = self.request.session.get('email')
        hashed_password = self.request.session.get('hashed_password')
        return (email and hashed_password) or phone

    def handle_no_permission(self):
        raise Http404()

    def create_owner(self):
        phone = self.request.session.get('phone')
        email = self.request.session.get('email')
        hashed_password = self.request.session.get('hashed_password')
        if email and hashed_password:
            return Owner(email=email, password=hashed_password)
        elif phone:
            return Owner(phone=phone)

    @transaction.atomic
    def form_valid(self, form):
        owner = self.create_owner()
        address = form.save()  # It's an `Address Form model`
        store = Store.objects.create(
            name=form.cleaned_data['store_name'],
            address=address
        )
        owner.store = store
        owner.save()
        self.request.session.flush()
        login(self.request, owner)
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
        'store_section': 'active',
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
        'store_section': 'active',
        'staff_selected': 'active',
    }
    success_url = reverse_lazy('accounts:user-address-list')

    def get_queryset(self):
        staff = Staff.get_staff(user=self.request.user)
        return staff.store.staffs.exclude(id=staff.id)


class StaffDetailView(PermissionRequiredMixin, IsStaffOfOwnerStore, DetailView):
    permission_required = ['vendors.view_staff']
    template_name = 'accounts/dashboard/dashboard.html'
    context_object_name = 'staff'
    extra_context = {
        'store_section': 'active',
        'staff_selected': 'active',
    }
    model = Staff


class StaffUpdateView(PermissionRequiredMixin, IsStaffOfOwnerStore, UpdateView):
    permission_required = ['vendors.change_staff']
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'store_section': 'active',
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


class StoreDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ['vendors.view_store']
    model = Store
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'store_section': 'active',
        'store_detail_section': 'active',
    }
    context_object_name = 'store'

    def get_object(self, queryset=None):
        staff = Staff.get_staff(self.request.user)
        return staff.store


class StoreUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['vendors.change_store']
    model = Store
    form_class = StoreForm
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'store_section': 'active',
        'form_section': 'active'
    }
    success_url = reverse_lazy('vendors:store-detail')

    def get_object(self, queryset=None):
        staff = Staff.get_staff(self.request.user)
        return staff.store

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        initial = {
            "store_name": self.get_object().name,
            **model_to_dict(self.get_object().address)
        }
        kwargs['initial'] = initial
        print('%' * 50, initial)
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        store_name = form.cleaned_data.pop('store_name', None)
        self.object.name = store_name
        for field, value in form.cleaned_data.items():
            setattr(self.object.address, field, value)
        self.object.save()
        self.object.address.save()
        response = HttpResponseRedirect(self.get_success_url())
        messages.success(self.request, f"StoreUpdateView")
        return response


class StoreDiscountListView(PermissionRequiredMixin, ListView):
    permission_required = ['products.view_storediscount']
    model = StoreDiscount
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'store_discount_section': 'active'}
    context_object_name = 'store_discount_list'

    def get_queryset(self):
        staff = Staff.get_staff(user=self.request.user)
        return self.model.objects.filter(store=staff.store)


class StoreDiscountCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['products.add_storediscount']
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


class StoreDiscountUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['products.change_storediscount']
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


class StoreDiscountDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['products.delete_storediscount']
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


class SelectProductView(PermissionRequiredMixin, FormView):
    """To create a new `StoreProduct` you need to provide `Product` first. """
    permission_required = ['products.add_storeproduct']
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


class StoreProductsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['products.add_storeproduct']
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


class SelectCategoryListView(PermissionRequiredMixin, ListView):
    permission_required = ['products.add_product']
    model = Category
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {'dashboard_category_select_section': True}

    def get(self, request, *args, **kwargs):
        if category_slug := self.request.GET.get('category_slug'):
            category = get_object_or_404(self.model, slug=category_slug)
            if not self.model.objects.filter(parent_category=category).exists():
                return redirect(f"{reverse('vendors:product-create')}?category_slug={category.slug}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if category_slug := self.request.GET.get('category_slug'):
            return self.model.objects.filter(parent_category__slug=category_slug)
        return self.model.objects.filter(parent_category=None)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['products.add_product']
    model = Product
    form_class = ProductForm
    template_name = 'accounts/dashboard/dashboard.html'
    success_url = reverse_lazy('vendors:store-product-create--select-product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # this prevents to open 'form section' in the dashboard.html
        context.pop('form', None)

        context['product_form'] = ProductForm()
        return context

    def get_category(self):
        return get_object_or_404(Category, slug=self.request.GET.get('category_slug'))

    @transaction.atomic
    def form_valid(self, form):
        product = form.save(commit=False)
        product.category = self.get_category()
        product.save()
        for field, value in form.cleaned_data.items():
            if isinstance(value, InMemoryUploadedFile):
                ProductImage.objects.create(product=product, image=value)
        messages.success(self.request, f"ProductCreateView")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class OrderItemListView(PermissionRequiredMixin, ListView):  # todo : ddddoinnngg
    permission_required = ['orders.view_order']
    model = OrderItem
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'staff_dashboard__order_section': 'active',
        'order_item_section_list': True,
    }
    context_object_name = 'order_item_list'

    def get_queryset(self):
        staff = Staff.get_staff(user=self.request.user)
        qs = super(
        ).get_queryset(
        ).select_related(
            'order', 'store_product'
        ).filter(
            store_product__store=staff.store,
            order__is_paid=True
        ).order_by('created_at')

        return qs


class OrderItemDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ['orders.view_order']
    model = OrderItem
    template_name = 'accounts/dashboard/dashboard.html'
    extra_context = {
        'staff_dashboard__order_section': 'active',
        'order_item_detail_section': 'active'
    }
    context_object_name = 'order_item'


class OrderItemUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['orders.change_order']
    model = OrderItem
    form_class = OrderItemStatusUpdateForm
    template_name = 'accounts/dashboard/dashboard.html'

    def get_success_url(self):
        return reverse('vendors:order-item-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[OrderItemDetailView.context_object_name] = self.get_object()
        context['staff_dashboard__order_section'] = 'active'
        context['order_item_update_section'] = 'active'
        context['change_status_form'] = context['form']
        context['form'] = None
        return context
