from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductColor,
    ProductImage,
    StoreProduct,
    Color,
    Rating,
    Discount,
    Coupon,
    Comment
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'parent_category', 'slug']
    readonly_fields = ['slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["category", "name", "description", "is_available", "slug",
              "rating_count", "rating_avg"]
    readonly_fields = ["slug", "rating_count", "rating_avg"]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass
    list_display = ['id', 'str_display']

    def str_display(self, obj):
        return str(obj)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass


@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
    # fields = []
    # readonly_fields = []
