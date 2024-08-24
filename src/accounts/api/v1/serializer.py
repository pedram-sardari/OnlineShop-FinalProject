from rest_framework import serializers

from accounts.models import UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        exclude = ['created_at', 'updated_at', 'is_deleted', 'is_default', 'user', 'label']
