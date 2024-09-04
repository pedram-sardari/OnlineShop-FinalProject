from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import User, UserAddress
import website.admin as website_admin


class UserAddressInline(admin.TabularInline):
    model = UserAddress
    list_display = ('id', 'label', 'is_deleted', 'is_default',
                    'province', 'city', 'neighborhood', 'zipcode')
    # can_delete = False
    extra = 1


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
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
    list_display = ["id", "email", "phone", "first_name", "last_name", "gender", "is_deleted", "is_active", "is_staff"]
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "gender")
    search_fields = ("first_name", "last_name", "email", "phone")
    ordering = ("email",)
    readonly_fields = ['last_login', 'date_joined', 'date_modified']
    inlines = [UserAddressInline]


@admin.register(UserAddress)
class CustomUserAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_user', 'label', 'is_deleted', 'is_default',
                    'province', 'city', 'neighborhood', 'zipcode')
    list_select_related = ['user']
    search_fields = ('user__email', 'province', 'city', 'neighborhood', 'zipcode')
    list_filter = ['province', 'city', 'neighborhood']
    actions = [website_admin.soft_delete, website_admin.remove_soft_delete]

    def display_user(self, obj):
        link = reverse('admin:accounts_user_change', args=(obj.user.id,))
        return format_html('<a href="{}">{}</a>', link, obj.user)

    display_user.short_description = 'User'

    def get_queryset(self, request):
        return UserAddress.objects.all_objects()  # todo: remove after testings
