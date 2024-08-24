from rest_framework import serializers

from products.models import StoreProduct


class StoreProductVendorsSerializer(serializers.ModelSerializer):
    discount = serializers.FloatField(source='get_discount')
    store = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = StoreProduct
        fields = ['id', 'store', 'discount', 'price']


class StoreProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    image = serializers.ImageField(source='product.get_default_image')
    color = serializers.CharField(source='product_color.color.value')

    class Meta:
        model = StoreProduct
        fields = ['id', 'name', 'price', 'store_discount', 'image', 'color']

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
