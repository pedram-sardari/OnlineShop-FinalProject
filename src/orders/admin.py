from django.contrib import admin

from accounts.models import UserAddress
from .models import Order, OrderItem, Cart, CartItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total')
    fields = ['customer', 'is_paid', 'status', 'user_address', 'cash_coupon_discount', 'total']
    readonly_fields = ['cash_coupon_discount', 'total']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user_address":
            kwargs["queryset"] = UserAddress.objects.all_addresses()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(OrderItem)
class OrderItemsAdmin(admin.ModelAdmin):
    fields = ['order', 'store_product', 'quantity', 'price', 'cash_discount', 'total']
    readonly_fields = ['price', 'cash_discount', 'total']


@admin.register(Cart)
class CartAdmin(OrderAdmin):
    pass


@admin.register(CartItem)
class CartItemAdmin(OrderItemsAdmin):
    pass
