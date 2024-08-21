from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from customers.models import Customer
from vendors.models import Store
from website.models import Address, CreateUpdateDateTimeFieldMixin
from . import utils
from website.manager import SoftDeleteManager

User = get_user_model()


class Discount(CreateUpdateDateTimeFieldMixin, models.Model):
    cash_discount = models.PositiveIntegerField(verbose_name=_("تخفیف نقدی"), default=0, blank=True)
    percentage_discount = models.PositiveIntegerField(
        verbose_name=_("تخفیف درصدی"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        default=0,
        help_text=_("عدد وارد شده باید بین 0 و 100 باشد.")
    )
    expiration_date = models.DateTimeField(verbose_name=_("زمان انقضا"))
    is_active = models.BooleanField(verbose_name=_("فعال"), default=True)

    # todo: validate both 'cash_discount' and 'percentage_discount' are not set 0

    class Meta:
        verbose_name = _("تخفیف")
        verbose_name_plural = _("تخفیفات")

    def get_final_cash_discount(self, price=0):
        return self.cash_discount + round((self.percentage_discount / 100) * price)

    def get_final_percentage_discount(self, price=0):
        pass  # todo: implementation

    def __str__(self):
        if self.cash_discount and self.percentage_discount:
            return f"{self.percentage_discount}% - {self.cash_discount} تومان "
        return f"{self.percentage_discount}%" or f"{self.cash_discount}%"


class StoreDiscount(Discount):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='store_discounts',
        verbose_name=_("فروشگاه")
    )

    class Meta:
        verbose_name = _("تخفیف فروشگاه")
        verbose_name_plural = _("تخفیفات فروشگاه")


class Coupon(models.Model):
    code = models.CharField(
        verbose_name=_("کد تخفیف"),
        max_length=100,
        null=True,
        blank=True,
        unique=True,
        help_text=_("این کد تخفیف باید یگانه باشد و در صورتی که خالی در نظر گرفته شود سیستم یک کد رندوم میسازد")
    )
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name="coupons", verbose_name=_("تخفیف"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="coupons", verbose_name=_("مشتری"))

    class Meta:
        verbose_name = _("کوپن تخفیف")
        verbose_name_plural = _("کوپن های تخفیف")
        unique_together = ("discount", "customer")

    def get_final_cash_discount(self, price):
        return self.discount.get_final_cash_discount(price=price)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = utils.generate_random_code()
        # todo: what if your code is duplicated
        # while True:
        #     if not self.code:
        #         self.code = utils.generate_random_code()
        #     if not Coupon.objects.filter(code=self.code).exists():
        #         break
        #     try:
        #         with transaction.atomic():
        #             super().save(*args, **kwargs)
        #         break
        #     except IntegrityError as e:
        #         if 'UNIQUE constraint failed:' in str(e):
        #             continue
        #         raise
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code or f"coupon-{self.id}"


class Category(CreateUpdateDateTimeFieldMixin, models.Model):
    name = models.CharField(_("نام دسته بندی"), max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, allow_unicode=True)
    description = models.TextField(_("توضیحات"), null=True, blank=True)
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_categories",
        null=True, blank=True,
        verbose_name=_("دسته بندی والد")
    )

    class Meta:
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")

    def can_be_a_subcategory(self, max_depth=3):
        pass  # todo: implementation

    @property
    def category_parent_list(self, include_child=True):
        categories = []
        current_category = self if include_child else self.parent_category
        while current_category is not None:
            categories.insert(0, current_category)
            current_category = current_category.parent_category
        return categories

    def set_slug(self):
        if not self.id or self.slug != slugify(self.name, allow_unicode=True):
            self.slug = slugify(self.name, allow_unicode=True)

    def save(self, *args, **kwargs):
        self.set_slug()
        self.can_be_a_subcategory()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(CreateUpdateDateTimeFieldMixin, models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("دسته بندی")
    )
    colors = models.ManyToManyField(
        "Color",
        related_name="products",
        blank=True,
        verbose_name=_("رنگ ها"),
        through='ProductColor'
    )

    name = models.CharField(_("نام محصول"), max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, allow_unicode=True)
    description = models.TextField(_("توضیحات"), null=True, blank=True)
    is_available = models.BooleanField(_("موجود است؟"), default=True)
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
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")

    def get_default_image(self):
        default_product_image = self.images.filter(is_default=True).first()
        if default_product_image:
            return default_product_image.image
        return None

    @property
    def inventory(self):
        return  # todo: implementation

    def update_rating_avg(self):
        if self.rating_count > 0:
            self.rating_avg = round(self.rating_sum / self.rating_count, 1)
        else:
            self.rating_avg = 0
        self.save()

    def set_slug(self):
        if not self.id or self.slug != slugify(self.name, allow_unicode=True):
            self.slug = slugify(self.name, allow_unicode=True)

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    def profile_image_upload_to(instance, filename):
        return f"product_images/{filename}"  # todo: create directory

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name=_("محصول"))
    image = models.ImageField(_("تصویر"), upload_to=profile_image_upload_to)  # todo: multiple image with content type
    is_default = models.BooleanField(verbose_name=_("تصویر پیش فرض"),
                                     default=False)  # todo: each product should only have ONE default address

    class Meta:
        verbose_name = _("تصویر محصول")
        verbose_name_plural = _("تصاویر محصولات")

    def set_default(self):
        if default_product_image := self.product.images.filter(is_default=True).first():
            if default_product_image.id != self.id:
                default_product_image.is_default = False
                default_product_image.save()

    def save(self, *args, **kwargs):
        if self.is_default:
            self.set_default()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.image)


class StoreProduct(CreateUpdateDateTimeFieldMixin, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="store_products",
                                verbose_name=_("محصول"))
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_products", verbose_name=_("فروشگاه"))
    store_discount = models.ForeignKey(
        StoreDiscount,
        on_delete=models.SET_NULL,
        related_name="store_products",
        null=True,
        blank=True,
        verbose_name=_("تخفیف")
    )
    price = models.PositiveIntegerField(_('قیمت'), default=0)
    is_available = models.BooleanField(_("موجود است؟"), default=True)
    inventory = models.PositiveIntegerField(_("تعداد موجودی"), default=1, validators=[MinValueValidator(1)])
    # todo: if an order finished, it must be decreased by 1
    # todo: if an order canceled, it must be increased by 1
    product_color = models.ForeignKey(
        'ProductColor',
        on_delete=models.SET_NULL,
        related_name='store_products',
        null=True,
        blank=True,
        verbose_name=_("رنگ محصول")
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user has deleted its account.")
    )

    objects = SoftDeleteManager()

    class Meta:
        verbose_name = _("محصول فروشگاه")
        verbose_name_plural = _("محصولات فروشگاه")

    def get_discount(self):
        return self.store_discount.percentage_discount if self.store_discount else None

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def delete(self, *args, soft_delete=False, **kwargs):
        if soft_delete:
            self.soft_delete()
        else:
            super().delete(*args, *kwargs)

    def __str__(self):
        return f"{self.product}-{self.store}"


class Color(models.Model):
    value = models.CharField(_("رنگ"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("رنگ")
        verbose_name_plural = _("رنگ ها")

    def __str__(self):
        return self.value


class ProductColor(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product",
        verbose_name=_("محصول")
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        related_name="product_color",
        verbose_name=_("رنگ")
    )

    class Meta:
        verbose_name = _("رنگ محصول")
        verbose_name_plural = _("رنگ های محصولات")
        unique_together = ("product", "color")

    def __str__(self):
        return f"{self.product} - {self.color}"


class Comment(CreateUpdateDateTimeFieldMixin, models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", _("ثبت شده")
        UNDER_REVIEW = "under review", _("درحال بررسی")
        APPROVED = "approved", _("تائید شده")
        REJECTED = "rejected", _("رد شده")

    title = models.CharField(_("عنوان نظر"), max_length=100)
    text = models.TextField(_("متن نظر"))
    status = models.CharField(_("وضعیت"), choices=Status.choices, max_length=15, default=Status.SUBMITTED)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("کاربر"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("محصول")
    )

    class Meta:
        verbose_name = _("نظر")
        verbose_name_plural = _("نظرات")

    def __str__(self):
        return self.title


class Rating(CreateUpdateDateTimeFieldMixin, models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("کاربر"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("محصول")
    )
    score = models.PositiveSmallIntegerField(
        _("امتیاز"),
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        verbose_name = _("امتیاز")
        verbose_name_plural = _("امتیازات")
        unique_together = ("customer", "product")

    def add_rating_to_product(self):
        if self.id:
            # todo: handle invalid id!
            old_rating = Rating.objects.get(id=self.id)
            self.product.rating_sum -= old_rating.score
        else:
            self.product.rating_count += 1
        self.product.rating_sum += self.score
        self.product.update_rating_avg()

    def remove_rating_from_product(self):
        if self.id:
            # todo: handle invalid id!
            old_rating = Rating.objects.get(id=self.id)
            self.product.rating_sum -= old_rating.score
            self.product.rating_count -= 1
            self.product.update_rating_avg()

    def save(self, *args, **kwargs):
        self.add_rating_to_product()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.remove_rating_from_product()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{str(self.customer)} | {self.product.name} | {self.score}"
