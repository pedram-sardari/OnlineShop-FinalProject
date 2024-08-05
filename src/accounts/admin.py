from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserAddress


class CustomUserAdmin(UserAdmin):
    model = User
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
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    readonly_fields = ['last_login', 'date_joined', 'date_modified']


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserAddress)
