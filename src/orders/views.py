from django.views.generic import TemplateView

from accounts.forms import UserAddressForm


class CartTemplateView(TemplateView):
    template_name = 'orders/cart.html'
    extra_context = {'create_new_address_form': UserAddressForm()}

