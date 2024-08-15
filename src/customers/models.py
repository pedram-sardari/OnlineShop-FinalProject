from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from website.constants import UserType

User = get_user_model()


class Customer(User):
    balance = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("مشتری")
        verbose_name_plural = _("مشتریان")

    @classmethod
    def is_customer(cls, user):
        return cls.objects.filter(id=user.id).exists()

    @classmethod
    def get_customer(cls, user):
        return cls.objects.filter(id=user.id).first()

    def has_ordered_store_product(self, store_product):
        return self.orders.filter(order_items__store_product=store_product).exists()

    def has_rated_store_product(self, store_product):
        return store_product.product.ratings.filter(customer=self).exists()

    def set_group(self):
        group = Group.objects.get(name=UserType.CUSTOMER)
        self.groups.add(group)

    def save(self, *args, **kwargs):
        self.is_staff = False  # NOQA
        self.is_superuser = False  # NOQA
        super().save(*args, **kwargs)
        self.set_group()
