from django.conf import settings
from django.http import HttpRequest

from orders.models import Cart, CartItem


def sync_session_and_db_carts(request: HttpRequest, customer):
    #  get or create db cart
    #  if created db cart
    #  get session cart items
    #  fill db cart with session cart Items
    #  delete session cart items

    session_cart_items = request.session.get(settings.SESSION_CART_KEY)
    print('?'*50, session_cart_items)
    try:
        db_cart = Cart.objects.get(customer=customer)

        if session_cart_items:
            for session_cart_item in session_cart_items:
                cart_item, created = CartItem.objects.get_or_create(order=db_cart,
                                                                    store_product_id=session_cart_item.get(
                                                                        'store_product'))  # todo: LM How to update without getting
                if created:
                    print('!' * 50, session_cart_item)
                    print('!' * 50, cart_item)
                    cart_item.quantity = session_cart_item['quantity']
                else:
                    print('9' * 50, session_cart_item)
                    print('9' * 50, cart_item)
                    cart_item.quantity += session_cart_item['quantity']
                cart_item.save()

    except Cart.DoesNotExist:
        db_cart = Cart.objects.create(customer=customer, user_address=customer.get_default_user_address())

        if session_cart_items:
            for session_cart_item in session_cart_items:
                CartItem.objects.create(order=db_cart, store_product_id=session_cart_item.get('store_product'))

