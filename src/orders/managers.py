from django.db import models


class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
        # return super().get_queryset().filter(is_paid=True) # todo: uncoment


class OrderItemManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().filter(order__is_paid=True)
        return super().get_queryset().filter()


class CartManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_paid=False)


class CartItemManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().filter(order__is_paid=False)
        return super().get_queryset().filter()
