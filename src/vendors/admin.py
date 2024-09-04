from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

import products.admin as products_admin
from accounts.admin import CustomUserAdmin
from .models import Staff, Store, Owner, Manager, Operator


class StaffInline(admin.TabularInline):
    model = Staff
    exclude = ['password', 'user_permissions']
    show_change_link = True
    extra = 1

    def has_add_permission(self, request, obj=None):
        return False

    #
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Staff)
class StaffAdmin(CustomUserAdmin):
    model = Staff
    fieldsets = (
        (_("Account Info"), {"fields": ("email", "phone", "password")}),
        (_("Personal Info"), {
            "fields": ("first_name", "last_name", "date_of_birth", "national_id",
                       "gender", "image")}),
        (
            _("Access"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_deleted",
                    "groups",
                    "user_permissions",
                    # "addresses" # todo: add new addresses in user admin change page
                ),
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", 'date_joined', 'date_modified')}),
        (_("Staff Info"), {"fields": ("role", "store")})
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "store"),
            },
        ),
    )
    list_display = CustomUserAdmin.list_display + ['role', 'display_store']
    list_select_related = ['store']

    @admin.display(ordering='store__id', description='store')
    def display_store(self, obj):
        link = reverse('admin:vendors_store_change', args=(obj.store.id,))
        return format_html('<a href="{}">{}</a>', link, obj.store)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.set_group()


@admin.register(Owner)
class OwnerAdmin(StaffAdmin):

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.set_group()


@admin.register(Manager)
class ManagerAdmin(StaffAdmin):

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.set_group()


@admin.register(Operator)
class OperatorAdmin(StaffAdmin):

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.set_group()


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'manager', 'operator', 'rating_avg')
    fields = ['name', 'description', 'address', 'order_count', 'slug', 'rating_avg', 'rating_count']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['order_count', 'slug','rating_avg', 'rating_count']
    inlines = [StaffInline, products_admin.StoreDiscountInline, products_admin.StoreProductInline]

    def owner(self, obj):
        return obj.staffs.filter(role=Staff.Roles.OWNER).first()

    owner.short_description = _('Store Owner')

    def manager(self, obj):
        return [str(manager_obj) for manager_obj in obj.staffs.filter(role=Staff.Roles.MANAGER)]

    manager.short_description = _('Product Manager')

    def operator(self, obj):
        return [str(operator_obj) for operator_obj in obj.staffs.filter(role=Staff.Roles.OPERATOR)]

    operator.short_description = _('Operator')
