from rest_framework import serializers

from accounts.api.v1.serializer import UserAddressSerializer
from orders.models import CartItem, Cart
from products.api.v1.serializer import StoreProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['store_product', 'quantity']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['store_product'] = StoreProductSerializer(instance.store_product, context=self.context).data
        return representation

    def create(self, validated_data):
        cart = self.context.get('cart')
        store_product = validated_data.get('store_product')
        cart_item, created = CartItem.objects.get_or_create(order=cart, store_product=store_product)
        cart_item.quantity = validated_data.get('quantity')
        cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', 0)
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(source='order_items', many=True)

    class Meta:
        model = Cart
        fields = ['user_address', 'cart_items']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print('==' * 50, instance)
        representation['cart_items'] = CartItemSerializer(CartItem.objects.filter(order_id=instance.id),
                                                          many=True,
                                                          context=self.context).data
        representation['user_address'] = UserAddressSerializer(instance.user_address).data
        return representation

    def update(self, instance, validated_data):
        # print('up' * 50, instance)
        customer = self.context.get('customer')
        # print('adr' * 50, validated_data)
        user_address = validated_data.get('user_address')
        address = customer.addresses.get(id=user_address.id)
        instance.user_address = address
        instance.save()
        return instance
