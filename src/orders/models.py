from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import UserAddress
from customers.models import Customer
from products.models import StoreProduct
from products.utils import generate_random_code
from website.models import CreateUpdateDateTimeFieldMixin, Address
from .managers import OrderManager, OrderItemManager, CartManager, CartItemManager


class Order(CreateUpdateDateTimeFieldMixin, models.Model):
    cash_coupon_discount = models.PositiveIntegerField(_("کوپن تخفیف"), default=0)
    order_number = models.CharField(_("order number"), max_length=10, unique=True, default=generate_random_code)
    is_paid = models.BooleanField(_("پرداخت شده"), default=False)
    total = models.PositiveIntegerField(_("جمع کل"), default=0)
    user_address = models.ForeignKey(
        UserAddress,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("آدرس"),
        null=True,
        blank=True
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("مشتری")
    )
    created_at = models.DateTimeField(_("Date of submitting"), default=timezone.now)

    objects = OrderManager()

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارشات")

    def update_total(self):
        self.total = self.order_items.aggregate(
            sum=Coalesce(
                Sum('total'), Value(0)
            )
        )['sum']
        self.save()


class OrderItem(CreateUpdateDateTimeFieldMixin, models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        DELIVERED = "delivered", _("Delivered")
        RETURNED = "returned", _("Returned")
        CANCELED = "canceled", _("Canceled")

    status = models.CharField(_("status"), choices=Status.choices, max_length=15, default=Status.ACTIVE)
    price = models.PositiveIntegerField(_('قیمت'), default=0)
    cash_discount = models.PositiveIntegerField(_("تخفیف (به تومان)"), default=0)
    quantity = models.PositiveSmallIntegerField(_("تعداد"), default=1,
                                                validators=[MinValueValidator(1)])  # todo: check quantity
    total = models.PositiveIntegerField(_("جمع"), default=0)
    store_product = models.ForeignKey(
        StoreProduct,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name=_("محصول فروشگاه")
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_("سفارش")
    )
    created_at = models.DateTimeField(_("Date of submitting"), default=timezone.now)
    objects = OrderItemManager()

    class Meta:
        verbose_name = _("قلم سفارش")
        verbose_name_plural = _("اقلام سفارشات")

    def increase_quantity_by_one(self):
        if (self.quantity + 1) <= 100:
            self.quantity += 1
            self.save()

    def decrease_quantity_by_one(self):
        if (self.quantity - 1) >= 1:
            self.quantity -= 1
            self.save()

    def update_calculative_fields(self):
        self.price = self.store_product.price
        if self.store_product.store_discount:
            self.cash_discount = self.store_product.store_discount.get_cash_discount(self.price)
        self.total = self.price * self.quantity - self.cash_discount

    def save(self, *args, **kwargs):
        self.update_calculative_fields()
        # TODO: don't let the discounted_price to become greater than 'Price' in updates
        super().save(*args, **kwargs)
        self.order.update_total()


class Cart(Order):
    objects = CartManager()

    class Meta:
        proxy = True
        verbose_name = _("سبد خرید")
        verbose_name_plural = _("سبد های خرید")

    @classmethod
    def get_user_cart(cls, user):
        return cls.objects.filter(customer_id=user.id).first

    def convert_to_order(self):
        self.created_at = timezone.now()
        self.order_items.update(created_at=self.created_at)
        self.save(convert_to_order=True)

    def save(self, convert_to_order=False, *args, **kwargs):
        if convert_to_order:
            self.is_paid = True
        else:
            self.is_paid = False
        super().save(*args, **kwargs)


class CartItem(OrderItem):
    objects = CartItemManager()

    class Meta:
        proxy = True
        verbose_name = _("قلم سبد خرید")
        verbose_name_plural = _("اقلام سبدهای خرید")
