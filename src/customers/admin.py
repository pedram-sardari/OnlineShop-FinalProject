from django.contrib import admin
from .models import Customer
from django.utils.translation import gettext_lazy as _
from accounts.admin import CustomUserAdmin


@admin.register(Customer)
class CustomerAdmin(CustomUserAdmin):
    model = Customer
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
        (_("اطلاعات حساب"), {"fields": ("balance",)})
    )


