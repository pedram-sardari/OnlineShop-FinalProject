from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
import jdatetime

CITIES = [('tehran', _('تهران')), ('yazd', _('یزد'))]
PROVINCES = [('tehran', _('تهران')), ('yazd', _('یزد'))]


class CreateUpdateDateTimeFieldMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Address(CreateUpdateDateTimeFieldMixin, models.Model):
    province = models.CharField(
        _("province"),
        max_length=100,
        choices=PROVINCES
    )  # todo: province should defines the list of cities
    city = models.CharField(_("شهر"), max_length=100, choices=CITIES)  # todo: complete the list of cities
    neighborhood = models.CharField(_("محله"), max_length=100, blank=True)
    street = models.CharField(_("خیابان"), max_length=100, blank=True)
    alley = models.CharField(_("کوچه"), max_length=100, blank=True)
    no = models.CharField(_("پلاک"), max_length=100, blank=True)
    zipcode = models.CharField(_("کد پستی"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("آدرس")
        verbose_name_plural = _("آدرس ها")

    def __str__(self):
        return f"{self.province}-{self.city}-{self.neighborhood}-{self.street}-{self.alley}-{self.no}-{self.zipcode}"


class RatingFieldsAndMethodsMixin(models.Model):
    rating_count = models.PositiveIntegerField(_("تعداد امتیازات"), default=0)
    rating_sum = models.PositiveIntegerField(_("مجموع امتیازات"), default=0)
    rating_avg = models.DecimalField(
        verbose_name=_("میانگین امتیازات"),
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        default=0.0,
    )

    class Meta:
        abstract = True

    def update_rating_avg(self):
        if self.rating_count > 0:
            self.rating_avg = round(self.rating_sum / self.rating_count, 1)
        else:
            self.rating_avg = 0
        self.save()  # NOQA
