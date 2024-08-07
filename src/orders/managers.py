from django.db import models


class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_paid=True)


class OrderItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(order__is_paid=True)


class CartManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_paid=False)


class CartItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(order__is_paid=False)
