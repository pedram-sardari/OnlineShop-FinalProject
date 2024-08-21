from rest_framework import serializers

from customers.models import Customer
from orders.models import CartItem, Cart, Order, OrderItem
from products.models import StoreProduct


class CartItemSerializer(serializers.ModelSerializer):
    # store_product_id = serializers.IntegerField(source='store_product.id', read_only=True)

    # store_product_id = serializers.PrimaryKeyRelatedField(source='store_product.id', queryset=StoreProduct.objects.all())
    # store_product = serializers.PrimaryKeyRelatedField(queryset=StoreProduct.objects.all())

    class Meta:
        model = CartItem
        # fields = '__all__'
        # fields = ['store_product_id', 'quantity']
        fields = ['store_product', 'quantity']

    # def validate_store_product(self, store_product):
    #     try:
    #         CartItem.objects.get(store_product=store_product)
    #     except CartItem.DoesNotExist:
    #         return {}

    def validate(self, attrs):
        # attrs = super().validate(attrs)
        store_product = attrs.get('store_product')
        # print('%' * 50, attrs)
        # attrs['pppppp'] = 3
        # try:
        #     CartItem.objects.get(store_product=store_product)
        # except CartItem.DoesNotExist:
        #     return {}
        return attrs

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
    # order_items = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all(), many=True)
    # order_items = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all(), many=True)
    # order_items = CartItemSerializer(many=True, read_only=True)
    # cart_items = serializers.SerializerMethodField()
    cart_items = CartItemSerializer(source='order_items', many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_address', 'cart_items']
        # fields = '__all__'

    # def get_cart_items(self, cart):
    #     return cart.order_items.all()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation.pop('order_items')
        print('==' * 50, instance)
        representation['cart_items'] = CartItemSerializer(CartItem.objects.filter(order_id=instance.id),
                                                          many=True).data
        return representation

    # def validate(self, attrs):
    # # attrs['jjjjjjjj'] = 2
    # # remove empty cart items (validated in CartItemSerializer's validate method)
    # attrs['cart_items'] = [cart_item for cart_item in attrs.get('cart_items') if cart_item]
    # return attrs

    def create(self, validated_data):
        customer = Customer.get_customer(user=self.context.get('request').user)
        print('^^' * 50, customer)
        # print('^^'*50, request.user)
        validated_cart_items = validated_data.pop('order_items')
        validated_data.pop('user_address')
        user_address = customer.get_default_user_address()
        cart = Cart.objects.create(**validated_data, customer=customer, user_address=user_address)
        # print('%' * 50, validated_data)
        print('%' * 50, validated_cart_items)

        for validated_cart_item in validated_cart_items:
            print('%' * 50, validated_cart_item)
            CartItem.objects.create(**validated_cart_item, order=cart)
        return cart
        return Order.objects.all().first()
