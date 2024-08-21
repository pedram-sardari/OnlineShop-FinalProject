from rest_framework import serializers

from products.models import StoreProduct


class StoreProductVendorsSerializer(serializers.ModelSerializer):
    discount = serializers.FloatField(source='get_discount')
    store = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = StoreProduct
        fields = ['id', 'store', 'discount', 'price']
