from django.contrib import admin
from .models import Customer
from django.utils.translation import gettext_lazy as _
from accounts.admin import CustomUserAdmin


class CustomerAdmin(CustomUserAdmin):
    model = Customer
    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        (_("Personal info"), {
            "fields": ("first_name", "last_name", "date_of_birth", "national_id",
                       "gender", "image")}),
        (
            _("Permissions"),
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
        (_("Important dates"), {"fields": ("last_login", 'date_joined', 'date_modified')}),
        (_("financial details"), {"fields": ("balance",)})
    )


admin.site.register(Customer, CustomerAdmin)
