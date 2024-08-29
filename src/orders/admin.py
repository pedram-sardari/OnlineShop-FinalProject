from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from accounts.models import UserAddress
from .models import Order, OrderItem, Cart, CartItem


@admin.action(description="Deliver selected order items")
def deliver_order_items(modeladmin, request, queryset):
    queryset.update(status=OrderItem.Status.DELIVERED)


@admin.action(description="Cancel selected order items")
def cancel_order_items(modeladmin, request, queryset):
    queryset.update(status=OrderItem.Status.CANCELED)


@admin.action(description="Return selected order items")
def return_order_items(modeladmin, request, queryset):
    queryset.update(status=OrderItem.Status.RETURNED)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_customer', 'total', 'is_paid', 'cash_coupon_discount', 'user_address')
    list_select_related = ['user_address', 'customer']
    fields = ['customer', 'is_paid', 'user_address', 'cash_coupon_discount', 'total']
    readonly_fields = ['cash_coupon_discount', 'total']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user_address":
            kwargs["queryset"] = UserAddress.objects.all_objects()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description='customer')
    def display_customer(self, obj):
        link = reverse('admin:customers_customer_change', args=(obj.customer.id,))
        return format_html('<a href="{}">{}</a>', link, obj.customer)


@admin.register(OrderItem)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'store_product', 'quantity', 'status', 'display_order', 'display_is_paid')
    list_select_related = ['store_product']
    fields = ['order', 'store_product', 'quantity', 'price', 'cash_discount', 'total', 'status']
    readonly_fields = ['price', 'cash_discount', 'total']
    actions = [deliver_order_items, cancel_order_items, return_order_items]
    list_filter = ['status']

    @admin.display(description='order', ordering='order__id')
    def display_order(self, obj):
        link = reverse('admin:orders_order_change', args=(obj.order.id,))
        return format_html('<a href="{}">{}</a>', link, obj.order.id)

    @admin.display(description='is_paid', ordering='order__is_paid', boolean=True)
    def display_is_paid(self, obj):
        return obj.order.is_paid


@admin.register(Cart)
class CartAdmin(OrderAdmin):
    pass


@admin.register(CartItem)
class CartItemAdmin(OrderItemsAdmin):
    pass
