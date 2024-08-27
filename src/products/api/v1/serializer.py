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
    color = serializers.SerializerMethodField()

    class Meta:
        model = StoreProduct
        fields = ['id', 'name', 'price', 'store_discount', 'image', 'color']

    def get_color(self, instance):
        if instance.product_color:
            return instance.product_color.color.value
        return None

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

    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'order_count', 'product_count', 'created_at', 'active_days']

    def get_active_days(self, instance):
        timedelta = timezone.now() - instance.created_at
        return timedelta.days
