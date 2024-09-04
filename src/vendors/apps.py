from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VendorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendors'
    verbose_name = _('Store and Vendors Management')
