from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import RedirectURLMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from customers.models import Customer
from vendors.models import Owner


class IsAddressForLoggedInUser(UserPassesTestMixin):
    def test_func(self):
        selected_address = self.get_object()  # NOQA
        return self.request.user.addresses.contains(selected_address)  # NOQA


class IsStaffOfOwnerStore(UserPassesTestMixin):
    """Is the selected staff one of staffs of the owner's store?"""

    def test_func(self):
        if owner := Owner.get_owner(self.request.user):  # NOQA
            selected_staff = self.get_object()  # NOQA
            return owner.store.staffs.contains(selected_staff)
        return False


class IsNotAuthenticated(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated  # NOQA

    def handle_no_permission(self):
        messages.error(self.request, 'شما با یک حساب کاربری در حال حاضر وارد شده اید')  # NOQA
        return redirect('home')


class CustomRedirectURLMixin(RedirectURLMixin):
    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if Customer.is_customer(self.request.user):  # NOQA
            return resolve_url(settings.CUSTOMERS_LOGIN_REDIRECT_URL)
        else:
            return resolve_url(settings.STAFF_LOGIN_REDIRECT_URL)


class DjangoLoginDispatchMixin:
    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:  # NOQA
            redirect_to = self.get_success_url()  # NOQA
            if redirect_to == self.request.path:  # NOQA
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)  # NOQA
