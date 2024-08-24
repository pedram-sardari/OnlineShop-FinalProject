from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import Customer
from orders.models import Cart, CartItem
from products.api.v1.serializer import StoreProductSerializer
from products.models import StoreProduct
from .serializer import CartSerializer, CartItemSerializer


def create_session_cart_items_list(session):
    session[settings.SESSION_CART_KEY] = []
    return session[settings.SESSION_CART_KEY]


class SubmitOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        cart = Cart.objects.get(customer=Customer.get_customer(self.request.user))
        cart.convert_to_order()
        return Response({'message': 'Order has been paid'}, status=status.HTTP_200_OK)


class CartAPIView(APIView):
    model = Cart
    cart_dict = {
        "cart_items": []
    }

    def is_authenticated(self):
        if self.request.user.is_authenticated:
            if customer := Customer.get_customer(user=self.request.user):
                return customer
        return None

    def get_db_cart(self, customer):
        cart, created = Cart.objects.get_or_create(customer=customer)
        return cart

    def get(self, request, *args, **kwargs):
        if customer := self.is_authenticated():
            return self.detail_authenticated(customer)
        else:
            return self.detail_anonymous()

    def detail_authenticated(self, customer):
        """from db"""
        print('u' * 50, self.request.session.get(settings.SESSION_CART_KEY))
        cart = self.get_db_cart(customer)
        serializer = CartSerializer(cart, context={'request': self.request})
        return Response(serializer.data)

    def detail_anonymous(self):
        """from session"""
        print('&' * 50, self.request.session.get(settings.SESSION_CART_KEY))
        cart_items = self.request.session.get(settings.SESSION_CART_KEY)
        if not cart_items:
            cart_items = create_session_cart_items_list(self.request.session)
            self.request.session.save()

        for cart_item in cart_items:  # todo: don't hit for each cart item separately
            cart_item['store_product'] = StoreProductSerializer(
                StoreProduct.objects.get(id=cart_item.get('store_product')), context={'request': self.request}).data

        self.cart_dict['cart_items'] = cart_items
        return Response(self.cart_dict)

    def put(self, request, *args, **kwargs):
        if customer := self.is_authenticated():
            return self.update_authenticated(customer)
        else:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def update_authenticated(self, customer):
        cart = self.get_db_cart(customer)
        serializer = CartSerializer(cart, data=self.request.data,
                                    context={'customer': customer, 'request': self.request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        print('is_valid' * 10, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemAPIView(APIView):
    model = CartItem

    def is_authenticated(self):
        if self.request.user.is_authenticated:
            if customer := Customer.get_customer(user=self.request.user):
                return customer
        return None

    def get_db_cart(self, customer):
        cart, created = Cart.objects.get_or_create(customer=customer)
        return cart

    def get_db_cart_items(self, customer):  # todo remove it if it is only userd in cart Items
        cart = self.get_db_cart(customer)
        return self.model.objects.filter(order=cart)

    def get_session_cart(self, customer):
        pass

    def get(self, request, *args, **kwargs):
        if customer := self.is_authenticated():
            return self.list_authenticated(customer)
        else:
            return self.list_anonymous()

    def list_authenticated(self, customer):
        """from db"""
        cart_items_qs = self.get_db_cart_items(customer)
        serializer = CartItemSerializer(cart_items_qs, many=True, context={'request': self.request})
        return Response(serializer.data)

    def list_anonymous(self):
        """from session"""
        # serializer = CartItemSerializer(data=self.request.session.get(settings.SESSION_CART_KEY), many=True)
        print('&' * 50, self.request.session.get(settings.SESSION_CART_KEY))
        return Response(self.request.session.get(settings.SESSION_CART_KEY))

    def post(self, request, *args, **kwargs):
        if customer := self.is_authenticated():
            return self.create_authenticated(customer)
        else:
            return self.create_anonymous()

    def create_authenticated(self, customer):
        cart = self.get_db_cart(customer)
        serializer = CartItemSerializer(data=self.request.data, context={'cart': cart})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_anonymous(self):
        serializer = CartItemSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        new_cart_item = serializer.initial_data
        print('*' * 50, new_cart_item)
        cart_items = self.request.session.get(settings.SESSION_CART_KEY)
        if cart_items is None:
            cart_items = create_session_cart_items_list(self.request.session)
            cart_items.append(new_cart_item)
        else:
            # print('*' * 50, store_product_id_list)
            for cart_item in cart_items:
                if new_cart_item['store_product'] == cart_item['store_product']:
                    break
            else:
                cart_items.append(new_cart_item)
        # print('wi' * 50, self.request.session.get(settings.SESSION_CART_KEY))
        self.request.session.save()
        return Response(serializer.initial_data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        if customer := self.is_authenticated():
            return self.update_authenticated(customer)
        else:
            return self.update_anonymous(customer)

    def update_authenticated(self, customer):
        cart = self.get_db_cart(customer)
        cart_item = cart.order_items.get(store_product_id=self.request.data.get('store_product'))
        serializer = CartItemSerializer(cart_item, data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update_anonymous(self, customer):
        serializer = CartItemSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        updated_cart_item = serializer.initial_data
        print('*' * 50, updated_cart_item)
        cart_items = self.request.session.get(settings.SESSION_CART_KEY)
        # print('*' * 50, store_product_id_list)
        for cart_item in cart_items:
            if updated_cart_item['store_product'] == cart_item['store_product']:
                cart_item['quantity'] = updated_cart_item['quantity']
                break
        # print('wi' * 50, self.request.session.get(settings.SESSION_CART_KEY))
        self.request.session.save()
        return Response(serializer.initial_data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        if customer := self.is_authenticated():
            return self.destroy_authenticated(customer)
        else:
            return self.destroy_anonymous(customer)

    def destroy_authenticated(self, customer):
        cart = self.get_db_cart(customer)
        cart_item = cart.order_items.get(store_product_id=self.request.data.get('store_product'))
        cart_item.delete()
        return Response({'detail': "The resource got deleted."}, status=status.HTTP_204_NO_CONTENT)

    def destroy_anonymous(self, customer):
        deleted_cart_item = self.request.data
        # print('*' * 50, 'deleting', deleted_cart_item)
        cart_items = self.request.session.get(settings.SESSION_CART_KEY)
        # print('*' * 50, store_product_id_list)
        for cart_item in cart_items:
            if deleted_cart_item['store_product'] == cart_item['store_product']:
                cart_items.remove(cart_item)
                break
        # print('wi' * 50, self.request.session.get(settings.SESSION_CART_KEY))
        self.request.session.save()
        return Response({"detail": "The resource got deleted."}, status=status.HTTP_204_NO_CONTENT)
