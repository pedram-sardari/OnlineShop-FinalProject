from rest_framework import viewsets, status
from django.http.request import HttpRequest
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import Customer
from orders.models import Cart, CartItem, Order
# from .serializer import StoreProductVendorsSerializer
from products.models import StoreProduct
from .serializer import CartSerializer, CartItemSerializer
from django.conf import settings


class CartItemAPIView(APIView):
    model = CartItem

    def is_authenticated(self):
        if self.request.user.is_authenticated:
            if customer := Customer.get_customer(user=self.request.user):
                return customer
        return None

    def get_db_cart(self, customer):
        return Cart.objects.get(customer=customer)

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
        serializer = CartItemSerializer(cart_items_qs, many=True)
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
        new_cart_item = serializer.data
        print('*' * 50, new_cart_item)
        cart_items = self.request.session.get(settings.SESSION_CART_KEY)
        if cart_items is None:
            cart_items = self.request.session[settings.SESSION_CART_KEY] = []
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        if customer := self.is_authenticated():
            return self.update_authenticated(customer)
        else:
            return self.update_anonymous(customer)

    def update_authenticated(self, customer):
        cart = self.get_db_cart(customer)
        cart_item = cart.order_items.get(store_product_id=self.request.data.get('store_product'))
        serializer = CartItemSerializer(cart_item, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update_anonymous(self, customer):
        serializer = CartItemSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        updated_cart_item = serializer.data
        print('*' * 50, updated_cart_item)
        cart_items = self.request.session.get(settings.SESSION_CART_KEY)
        # print('*' * 50, store_product_id_list)
        for cart_item in cart_items:
            if updated_cart_item['store_product'] == cart_item['store_product']:
                cart_item['quantity'] = updated_cart_item['quantity']
                break
        # print('wi' * 50, self.request.session.get(settings.SESSION_CART_KEY))
        self.request.session.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        print('*' * 50, deleted_cart_item)
        cart_items = self.request.session.get(settings.SESSION_CART_KEY)
        # print('*' * 50, store_product_id_list)
        for cart_item in cart_items:
            if deleted_cart_item['store_product'] == cart_item['store_product']:
                cart_items.remove(cart_item)
                break
        # print('wi' * 50, self.request.session.get(settings.SESSION_CART_KEY))
        self.request.session.save()
        return Response({'detail': "The resource got deleted."}, status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = CartSerializer


class CartView(APIView):
    model = CartItem

    # permission_classes = [IsAuthenticated]
    def is_authenticated(self):
        if self.request.user.is_authenticated:
            if customer := Customer.get_customer(user=self.request.user):
                return customer
        return None

    def get(self, request, *args, **kwargs):
        if customer := self.is_authenticated():
            return self.retrieve_authenticated_user(customer)
        else:
            return self.retrieve_anonymous_user()

    def get_db_cart(self, customer):
        return self.model.objects.get(customer=customer)

    def get_session_cart(self, customer):
        pass

    def retrieve_authenticated_user(self, customer):
        """from db"""
        cart = self.get_db_cart(customer)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def retrieve_anonymous_user(self):
        """from session"""
        pass
