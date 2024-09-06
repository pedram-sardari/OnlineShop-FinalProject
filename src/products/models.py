from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from customers.models import Customer
from vendors.models import Store
from website.manager import SoftDeleteManager
from website.models import Address, CreateUpdateDateTimeFieldMixin, RatingFieldsAndMethodsMixin
from website.constants import RATING_CHOICES
from . import utils

User = get_user_model()


class Discount(CreateUpdateDateTimeFieldMixin, models.Model):
    cash_discount = models.PositiveIntegerField(verbose_name=_("cash discount"), default=0, blank=True)
    percentage_discount = models.PositiveIntegerField(
        verbose_name=_("percentage discount"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        default=0,
        help_text=_("The entered number must be between 0 and 100.")
    )
    expiration_date = models.DateTimeField(verbose_name=_("expiration date"))
    is_active = models.BooleanField(verbose_name=_("is active"), default=True)

    # todo: validate both 'cash_discount' and 'percentage_discount' are not set 0

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def get_cash_discount(self, price=0):
        final_cash_discount = self.cash_discount or round((self.percentage_discount / 100) * price)
        if price - final_cash_discount < 0:
            return -1
        return final_cash_discount

    def get_percentage_discount(self, price=0):
        final_percentage_discount = self.percentage_discount or round(self.cash_discount / price * 100)
        if final_percentage_discount > 100:
            return -1
        return final_percentage_discount

    def get_discounted_price(self, price):
        cash_discount = self.get_cash_discount(price)
        return price - cash_discount if cash_discount > 0 else 0

    def __str__(self):
        if self.percentage_discount:
            return f"{self.percentage_discount}%"
        return f"{self.cash_discount}{_("Toman")}"


# todo: discount !< product price
# todo: don't fill both cash and percentage
class StoreDiscount(Discount):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='store_discounts',
        verbose_name=_("store")
    )

    class Meta:
        verbose_name = _("Store Discount")
        verbose_name_plural = _("Store Discounts")


class Coupon(models.Model):
    code = models.CharField(
        verbose_name=_("Coupon"),
        max_length=100,
        null=True,
        blank=True,
        unique=True,
        help_text=_("This discount code must be unique and if "
                    "it is considered empty, the system will create a random code")

    )
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name="coupons", verbose_name=_("discount"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="coupons", verbose_name=_("customer"))

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")
        unique_together = ("discount", "customer")

    def get_final_cash_discount(self, price):
        return self.discount.get_cash_discount(price=price)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = utils.generate_random_code(digits=True, letters=True, length=12)
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
    def upload_to(instance, filename):  # todo: create directory
        return f"category_images/{filename}"

    name = models.CharField(_("category name"), max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, allow_unicode=True)
    description = models.TextField(_("description"), null=True, blank=True)
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_categories",
        null=True, blank=True,
        verbose_name=_("parent category")
    )
    image = models.ImageField(verbose_name=_("image"), upload_to=upload_to, null=True, blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

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


class Product(CreateUpdateDateTimeFieldMixin, RatingFieldsAndMethodsMixin, models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("category")
    )
    colors = models.ManyToManyField(
        "Color",
        related_name="products",
        blank=True,
        verbose_name=_("colors"),
        through='ProductColor'
    )

    name = models.CharField(_("product name"), max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, allow_unicode=True)
    description = models.TextField(_("description"), null=True, blank=True)
    is_available = models.BooleanField(_("is available"), default=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_default_image(self):
        default_product_image = self.images.filter(is_default=True).first() or self.images.all().first()
        if default_product_image:
            return default_product_image.image
        return None

    @property
    def inventory(self):
        return  # todo: implementation

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

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name=_("product"))
    image = models.ImageField(_("image"), upload_to=profile_image_upload_to)  # todo: multiple image with content type
    is_default = models.BooleanField(verbose_name=_("is default"),
                                     default=False)  # todo: each product should only have ONE default address

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Products Images")

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


class StoreProduct(CreateUpdateDateTimeFieldMixin, RatingFieldsAndMethodsMixin, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="store_products",
                                verbose_name=_("product"))
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_products", verbose_name=_("فروشگاه"))
    store_discount = models.ForeignKey(
        StoreDiscount,
        on_delete=models.SET_NULL,
        related_name="store_products",
        null=True,
        blank=True,
        verbose_name=_("store discount")
    )
    price = models.PositiveIntegerField(_('price'), default=0)
    is_available = models.BooleanField(_("is available"), default=True)
    inventory = models.PositiveIntegerField(_("inventory"), default=1, validators=[MinValueValidator(1)])
    # todo: if an order finished, it must be decreased by 1
    # todo: if an order canceled, it must be increased by 1
    product_color = models.ForeignKey(
        'ProductColor',
        on_delete=models.SET_NULL,
        related_name='store_products',
        null=True,
        blank=True,
        verbose_name=_("product color")
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user has deleted its account.")
    )

    objects = SoftDeleteManager()

    class Meta:
        verbose_name = _("Store Product")
        verbose_name_plural = _("Store Products")

    def get_discounted_price(self):
        return self.store_discount.get_discounted_price(self.price) if self.store_discount else None

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
    value = models.CharField(_("color name"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __str__(self):
        return self.value


class ProductColor(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product",
        verbose_name=_("product")
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        related_name="product_color",
        verbose_name=_("color")
    )

    class Meta:
        verbose_name = _("Product Color")
        verbose_name_plural = _("Product Colors")
        unique_together = ("product", "color")

    def __str__(self):
        return f"{self.color} - {self.product}"


class Comment(CreateUpdateDateTimeFieldMixin, models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", _("submitted")
        UNDER_REVIEW = "under review", _("under review")
        APPROVED = "approved", _("under review")
        REJECTED = "rejected", _("rejected")

    title = models.CharField(_("title"), max_length=100)
    text = models.TextField(_("text"))
    status = models.CharField(_("status"), choices=Status.choices, max_length=15, default=Status.SUBMITTED)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("customer"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("product")
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.title


class Rating(CreateUpdateDateTimeFieldMixin, models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("customer"),
    )
    store_product = models.ForeignKey(
        StoreProduct,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("محصول فروشگاهی")
    )
    score = models.PositiveSmallIntegerField(
        _("score"),
        choices=RATING_CHOICES,
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        unique_together = ("customer", "store_product")

    def add_rating(self, related_obj):
        if self.id:
            # todo: handle invalid id!
            old_rating = Rating.objects.get(id=self.id)
            related_obj.rating_sum -= old_rating.score
        else:
            related_obj.rating_count += 1
        related_obj.rating_sum += self.score
        related_obj.update_rating_avg()

    def remove_rating(self, related_obj):
        if self.id:
            # todo: handle invalid id!
            old_rating = Rating.objects.get(id=self.id)
            related_obj.rating_sum -= old_rating.score
            related_obj.rating_count -= 1
            related_obj.update_rating_avg()

    def save(self, *args, **kwargs):
        self.add_rating(related_obj=self.store_product)
        self.add_rating(related_obj=self.store_product.product)
        self.add_rating(related_obj=self.store_product.store)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.remove_rating(related_obj=self.store_product)
        self.remove_rating(related_obj=self.store_product.product)
        self.remove_rating(related_obj=self.store_product.store)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{str(self.customer)} | {self.store_product.product.name} | {self.score}"
