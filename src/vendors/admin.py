from django.contrib import admin
from .models import Staff, Store, Owner, Manager, Operator
from django.utils.translation import gettext_lazy as _
from accounts.admin import CustomUserAdmin


@admin.register(Staff)
class StaffAdmin(CustomUserAdmin):
    model = Staff
    fieldsets = (
        (_("اطلاعات حساب کاربری"), {"fields": ("email", "phone", "password")}),
        (_("اطلاعات شخصی"), {
            "fields": ("first_name", "last_name", "date_of_birth", "national_id",
                       "gender", "image")}),
        (
            _("دسترسی ها"),
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
        (_("تاریخ های مهم"), {"fields": ("last_login", 'date_joined', 'date_modified')}),
        (_("اطلاعات کارمند"), {"fields": ("role", "store")})
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


@admin.register(Owner)
class OwnerAdmin(StaffAdmin):
    pass


@admin.register(Manager)
class ManagerAdmin(StaffAdmin):
    pass


@admin.register(Operator)
class OperatorAdmin(StaffAdmin):
    pass


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'address', 'order_count', 'slug']
    readonly_fields = ['order_count', 'slug']
