from django.conf import settings
from django.http import HttpRequest

from orders.models import Cart, CartItem


def sync_session_and_db_carts(request: HttpRequest, customer):
    session_cart_items = request.session.get(settings.SESSION_CART_KEY)

    db_cart, created = Cart.objects.get_or_create(customer=customer)
    # if the current cart doesn't have any address and the user has default address
    # set their default address as the current cart's address
    if created or not db_cart.user_address:
        if default_address := customer.get_default_user_address():
            db_cart.user_address = default_address
            db_cart.save()

    if session_cart_items and created:
        for session_cart_item in session_cart_items:
            CartItem.objects.create(order=db_cart, store_product_id=session_cart_item.get('store_product'))
    elif session_cart_items and not created:
        for session_cart_item in session_cart_items:
            cart_item, created = CartItem.objects.get_or_create(order=db_cart,
                                                                store_product_id=session_cart_item.get(
                                                                    'store_product'))  # todo: LM How to update without getting
            if created:
                cart_item.quantity = int(session_cart_item['quantity'])
            else:
                cart_item.quantity += int(session_cart_item['quantity'])
            cart_item.save()
