from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Customer(User):
    balance = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("مشتری")
        verbose_name_plural = _("مشتریان")

    def save(self, *args, **kwargs):
        self.is_staff = False
        self.is_superuser = False
        super().save(*args, **kwargs)
