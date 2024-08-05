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
        _("استان"),
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


class JalaliDateField(models.DateField):

    def get_prep_value(self, value):
        if isinstance(value, jdatetime.date):
            return value.togregorian().date()
        return super().get_prep_value(value)

    def from_db_value(self, value, expression=None, connection=None, context=None):
        if value is None:
            return value
        return jdatetime.date.fromgregorian(date=value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, jdatetime.date):
            return value
        try:
            return jdatetime.date.fromgregorian(date=value)
        except (TypeError, ValueError):
            return jdatetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


class JalaliDateTimeField(models.DateTimeField):
    def get_prep_value(self, value):
        if isinstance(value, jdatetime.datetime):
            # Convert Jalali to Gregorian
            return value.togregorian()
        return super().get_prep_value(value)

    def from_db_value(self, value, expression=None, connection=None, context=None):
        if value is None:
            return value
        # Convert Gregorian to Jalali
        return jdatetime.datetime.fromgregorian(datetime=value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, jdatetime.datetime):
            return value
        try:
            # Convert to Jalali
            return jdatetime.datetime.fromgregorian(datetime=value)
        except (TypeError, ValueError):
            return super().to_python(value)
