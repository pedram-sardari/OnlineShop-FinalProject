from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from website.constants import UserType
from website.models import Address, CreateUpdateDateTimeFieldMixin
from .managers import OwnerStaffManager, ManagerStaffManager, OperatorStaffManager

User = get_user_model()


class Store(CreateUpdateDateTimeFieldMixin, models.Model):
    name = models.CharField(_("نام فروشگاه"), max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, allow_unicode=True)
    description = models.TextField(verbose_name=_("توضیحات"), null=True, blank=True)
    address = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        related_name="store",
        verbose_name=_('آدرس'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("فروشگاه")
        verbose_name_plural = _("فروشگاه ها")

    @property
    def order_count(self):
        from orders.models import OrderItem
        qs = self.store_products.filter(
            order_items__order__is_paid=True,
            order_items__status=OrderItem.Status.DELIVERED
        ).annotate(
            quantity=Sum("order_items__quantity")
        ).aggregate(
            quantity_sum=Sum("quantity", default=0)
        )
        return qs['quantity_sum']

    @property
    def product_count(self):
        return self.store_products.count()

    def set_slug(self):
        if not self.id or self.slug != slugify(self.name, allow_unicode=True):
            self.slug = slugify(self.name, allow_unicode=True)

    def save(self, *args, **kwargs):
        self.set_slug()
        super(Store, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Staff(User):
    class Roles(models.TextChoices):
        OWNER = UserType.OWNER, _("مدیر فروشگاه")
        MANAGER = UserType.MANAGER, _("مدیر محصول")
        OPERATOR = UserType.OPERATOR, _("ناظر")

    role = models.CharField(_("عنوان شغلی"), max_length=12, choices=Roles.choices, default=Roles.OPERATOR)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name=_("فروشگاه"), related_name='staffs')

    class Meta:
        verbose_name = _("کارمند")
        verbose_name_plural = _("کارمندان")

    @classmethod
    def get_staff(cls, user):
        return cls.objects.filter(id=user.id).first()

    @classmethod
    def is_staff(cls, user):
        return cls.objects.filter(id=user.id).exists()

    def set_group(self):
        if self.role == self.Roles.OWNER:
            group = Group.objects.get(name=self.Roles.OWNER)
        elif self.role == self.Roles.MANAGER:
            group = Group.objects.get(name=self.Roles.MANAGER)
        else:
            group = Group.objects.get(name=self.Roles.OPERATOR)
        self.groups.add(group)

    def save(self, *args, **kwargs):
        self.is_staff = True  # NOQA
        self.is_superuser = False  # NOQA
        super().save(*args, **kwargs)
        self.set_group()


class Owner(Staff):
    objects = OwnerStaffManager()

    class Meta:
        proxy = True
        verbose_name = _("مدیر فروشگاه")
        verbose_name_plural = _("مدیران فروشگاه")

    @classmethod
    def get_owner(cls, user):
        return cls.objects.filter(id=user.id).first()

    @classmethod
    def is_owner(cls, user):
        return cls.objects.filter(id=user.id).exists()

    def save(self, *args, **kwargs):
        self.role = self.Roles.OWNER
        super(Owner, self).save(*args, **kwargs)


class Manager(Staff):
    objects = ManagerStaffManager()

    class Meta:
        proxy = True
        verbose_name = _("مدیر محصول")
        verbose_name_plural = _("مدیران محصول")

    @classmethod
    def get_manager(cls, user):
        return cls.objects.filter(id=user.id).first()

    @classmethod
    def is_manager(cls, user):
        return cls.objects.filter(id=user.id).exists()

    def save(self, *args, **kwargs):
        self.role = self.Roles.MANAGER
        super().save(*args, **kwargs)


class Operator(Staff):
    objects = OperatorStaffManager()

    class Meta:
        proxy = True
        verbose_name = _("ناظر")
        verbose_name_plural = _("ناظران")

    @classmethod
    def get_operator(cls, user):
        return cls.objects.filter(id=user.id).first()

    @classmethod
    def is_operator(cls, user):
        return cls.objects.filter(id=user.id).exists()

    def save(self, *args, **kwargs):
        self.role = self.Roles.OPERATOR
        super().save(*args, **kwargs)
