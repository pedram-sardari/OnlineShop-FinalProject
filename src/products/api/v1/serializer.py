from urllib.parse import unquote

from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from rest_framework import serializers

from products.models import StoreProduct
from vendors.models import Store


class StoreProductVendorsSerializer(serializers.ModelSerializer):
    discount = serializers.FloatField(source='get_discount')
    store = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = StoreProduct
        fields = ['id', 'store', 'discount', 'price']


class StoreProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    image = serializers.ImageField(source='product.get_default_image')
    rating_avg = serializers.FloatField(source='product.rating_avg')
    rating_count = serializers.IntegerField(source='product.rating_count')
    store = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    discounted_price = serializers.IntegerField(source='get_discounted_price')
    color = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    order_count = serializers.SerializerMethodField()

    class Meta:
        model = StoreProduct
        fields = ['id', 'name', 'price', 'discounted_price', 'image', 'color', 'store', 'product', 'rating_avg',
                  'rating_count', 'url', 'order_count']

    def get_color(self, instance):
        if instance.product_color:
            return instance.product_color.color.value
        return None

    def get_url(self, instance):
        request = self.context.get('request')
        relative_url = reverse('products:product-detail', kwargs={'pk': instance.product.pk})
        return request.build_absolute_uri(relative_url)

    def get_order_count(self, instance):
        return instance.order_items.aggregate(Sum('quantity', default=0))['quantity__sum']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.product.get_default_image():
            image_url = self.context.get('request').build_absolute_uri(
                f"/media/{instance.product.get_default_image()}"
            )
        else:
            image_url = self.context.get('request').build_absolute_uri(
                '/static/products/img/product-default-image.png'
            )
        representation['image'] = image_url
        return representation


class StoreSerializer(serializers.ModelSerializer):
    active_days = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'order_count', 'product_count', 'created_at', 'active_days', 'url']

    def get_active_days(self, instance):
        timedelta = timezone.now() - instance.created_at
        return timedelta.days

    def get_url(self, instance):
        request = self.context.get('request')
        relative_url = reverse('products:store-product-list-in-store') + f'?store__slug={instance.slug}'
        return unquote(request.build_absolute_uri(relative_url))
