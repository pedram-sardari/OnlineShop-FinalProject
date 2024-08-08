from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from website.models import Address, CITIES, PROVINCES
from .models import Owner, Store
from .forms import OwnerRegisterForm


class OwnerRegisterView(UserPassesTestMixin, FormView):
    model = Owner
    template_name = 'accounts/register.html'
    form_class = OwnerRegisterForm
    success_url = reverse_lazy('login')
    extra_context = {'vendor_register': 'active'}

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, 'شما با یک حساب کاربری در حال حاضر وارد شده اید')
        return redirect('home')

    def form_valid(self, form):
        messages.success(self.request, f"Your account has been created successfully!")
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
        return super().form_valid(form)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)
