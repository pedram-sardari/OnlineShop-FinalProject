from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from website.models import Address, CreateUpdateDateTimeFieldMixin

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
    order_count = models.PositiveIntegerField(verbose_name=_("تعداد کل سفارشات"), default=0)

    def save(self, *args, **kwargs):
        self.set_slug()
        super(Store, self).save(*args, **kwargs)

    def set_slug(self):
        if not self.id or self.slug != slugify(self.name, allow_unicode=True):
            self.slug = slugify(self.name, allow_unicode=True)

    class Meta:
        verbose_name = _("فروشگاه")
        verbose_name_plural = _("فروشگاه ها")

    def __str__(self):
        return self.name


class Staff(User):
    class Roles(models.TextChoices):
        OWNER = "Owner", _("مدیر فروشگاه")
        MANAGER = "Manager", _("مدیر محصول")
        OPERATOR = "Operator", _("ناظر")

    role = models.CharField(_("سمت"), max_length=12, choices=Roles.choices, default=Roles.OPERATOR)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name=_("فروشگاه"), related_name='staff')

    class Meta:
        verbose_name = _("کارمند")
        verbose_name_plural = _("کارمندان")

    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_superuser = False
        super().save(*args, **kwargs)
