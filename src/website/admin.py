from django.contrib import admin

from .models import Address

admin.AdminSite.empty_value_display = '-'


@admin.action(description="is_deleted=True")
def soft_delete(modeladmin, request, queryset):
    queryset.update(is_deleted=True)


@admin.action(description="is_deleted=False")
def remove_soft_delete(modeladmin, request, queryset):
    queryset.update(is_deleted=False)


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'city', 'neighborhood', 'street', 'alley', 'no', 'zipcode')
    search_fields = ('province', 'city', 'neighborhood', 'zipcode')
    list_filter = ['province', 'city', 'neighborhood']

    # todo: add action to soft delete
