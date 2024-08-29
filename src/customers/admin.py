from django.contrib import admin
from django.utils.translation import gettext_lazy as _

import accounts.admin as accounts_admin
import products.admin as product_admin
from accounts.admin import CustomUserAdmin
from .models import Customer


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
    inlines = [accounts_admin.UserAddressInline, product_admin.OrderInline,
               product_admin.RatingInline, product_admin.CommentInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.set_group()
