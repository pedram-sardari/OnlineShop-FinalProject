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
    StoreDiscount,
    Coupon,
    Comment
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    fields = ['name', 'description', 'parent_category', 'slug']
    readonly_fields = ['slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
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


@admin.register(StoreDiscount)
class StoreDiscountAdmin(admin.ModelAdmin):
    pass
    list_display = ['id', 'str_display']

    def str_display(self, obj):
        return str(obj)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass


@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'store')

    def name(self, instance):
        return instance.product.name

    def get_queryset(self, request):
        return self.model.objects.all_objects()  # todo: remove after testings


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'product')
    # fields = []
    # readonly_fields = []
