from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

import website.admin as website_admin
from orders.models import Order
from .models import (
    Category,
    Product,
    ProductColor,
    ProductImage,
    StoreProduct,
    Color,
    Rating,
    Discount,
    StoreDiscount,
    Coupon,
    Comment
)


class StoreDiscountInline(admin.TabularInline):
    model = StoreDiscount
    extra = 1


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class OrderInline(admin.TabularInline):
    model = Order
    readonly_fields = ('is_paid', 'created_at',)
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1


class ProductInline(admin.StackedInline):
    model = Product
    raw_id_fields = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ('id', 'name')
    fields = ['name', 'description', 'parent_category', 'slug']
    readonly_fields = ['slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_category', 'is_available')
    list_select_related = ['category']
    inlines = [ProductImageInline, ProductColorInline]
    list_filter = ['category__name']
    search_fields = ['name', 'category__name']
    fields = ["category", "name", "description", "is_available", "slug",
              "rating_count", "rating_avg"]
    readonly_fields = ["slug", "rating_count", "rating_avg"]

    def display_category(self, obj):
        link = reverse('admin:products_category_change', args=(obj.category.id,))
        return format_html('<a href="{}">{}</a>', link, obj.category)

    display_category.short_description = 'Category'


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_product', 'color']
    list_select_related = ['product', 'color']

    @admin.display(ordering='product__name', description='product')
    def display_product(self, obj):
        link = reverse('admin:products_product_change', args=(obj.product.id,))
        return format_html('<a href="{}">{}</a>', link, obj.product)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_product', 'image', 'is_default']
    list_select_related = ['product', ]

    @admin.display(ordering='product__name', description='product')
    def display_product(self, obj):
        link = reverse('admin:products_product_change', args=(obj.product.id,))
        return format_html('<a href="{}">{}</a>', link, obj.product)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'cash_discount', 'percentage_discount', 'expiration_date', 'is_active']
    list_filter = ['cash_discount', 'percentage_discount', 'expiration_date', 'is_active']


@admin.register(StoreDiscount)
class StoreDiscountAdmin(admin.ModelAdmin):
    list_display = DiscountAdmin.list_display + ['store']
    list_select_related = ['store']
    search_fields = ['store']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'display_customer', 'display_discount']
    list_select_related = ['customer', 'discount']

    @admin.display(description='customer')
    def display_customer(self, obj):
        link = reverse('admin:customers_customer_change', args=(obj.customer.id,))
        return format_html('<a href="{}">{}</a>', link, obj.customer)

    def display_discount(self, obj):
        link = reverse('admin:products_discount_change', args=(obj.discount.id,))
        return format_html('<a href="{}">{}</a>', link, obj.discount)

    display_discount.short_description = 'discount'


@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_product', 'display_store', 'display_store_discount', 'price',
                    'inventory', 'product_color', 'is_available', 'is_deleted')
    actions = [website_admin.soft_delete, website_admin.remove_soft_delete]

    def name(self, instance):
        return instance.product.name

    def get_queryset(self, request):
        return self.model.objects.all_objects()  # todo: remove after testings

    @admin.display(ordering='store__id', description='store')
    def display_store(self, obj):
        link = reverse('admin:vendors_store_change', args=(obj.store.id,))
        return format_html('<a href="{}">{}</a>', link, obj.store)

    @admin.display(ordering='product__name', description='product')
    def display_product(self, obj):
        link = reverse('admin:products_product_change', args=(obj.product.id,))
        return format_html('<a href="{}">{}</a>', link, obj.product)

    @admin.display(description='store discount')
    def display_store_discount(self, obj):
        if obj.store_discount is not None:
            link = reverse('admin:products_storediscount_change', args=(obj.store_discount.id,))
            return format_html('<a href="{}">{}</a>', link, obj.store_discount)
        return '-'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'product')
    # fields = []
    # readonly_fields = []
