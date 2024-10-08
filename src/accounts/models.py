from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from website.manager import SoftDeleteManager
from website.models import Address
from website.validators import phone_validator, national_id_validator
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    def profile_image_upload_to(instance, filename):  # todo: create directory
        return f"user_images/{filename}"

    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    password = models.CharField(_("password"), max_length=128, null=True, blank=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)  # todo: last name >> نام خانوادگی
    email = models.EmailField(
        _("email"),
        unique=True,
        null=True,
        blank=True,
        default=None,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    phone = models.CharField(
        _("phone"),
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        default=None,
        validators=[phone_validator],
        error_messages={
            "unique": _("A user with that phone already exists."),
        },
    )
    national_id = models.CharField(
        _("national id"),
        max_length=24,
        unique=True,
        null=True,
        blank=True,
        validators=[national_id_validator],  # todo : regex validation
        error_messages={
            "unique": _("A user with that phone already exists."),
        },
    )
    gender = models.CharField(max_length=1, choices=Gender.choices, null=True, blank=True)
    is_staff = models.BooleanField(
        _("is staff"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_deleted = models.BooleanField(default=False,
                                     help_text=_("Designates whether this user has deleted its account."))
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    date_modified = models.DateTimeField(_("date modified"), auto_now=True)
    image = models.ImageField(verbose_name=_("image"), upload_to=profile_image_upload_to, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        indexes = [
            models.Index(fields=['is_deleted'])
        ]

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        if self.email:
            return self.email.split('@')[0]
        return ''

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_customer(self):
        return not self.is_staff

    @property
    def age(self):
        # todo: test user's age in jalali!
        # todo: test age functionality
        if self.date_of_birth is None:
            return None
        today = timezone.now().date()
        age = int(
            today.year
            - self.date_of_birth.year
            - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
        return age

    def get_default_user_address(self):
        return self.addresses.filter(is_default=True).first() or self.addresses.all().first()

    def save(self, *args, **kwargs):
        """Do not change is_superuser and is_staff attributes here because they are set in subclasses"""

        if not (self.email or self.phone):
            raise ValueError(_("Either email or phone must be set"))

        if self.email == "":
            self.email = None
        if self.phone == "":
            self.phone = None

        super().save(*args, **kwargs)

    def delete(self, *args, soft_delete=False, **kwargs):
        if soft_delete:
            self.is_deleted = True
            self.save()
        else:
            super().delete(*args, *kwargs)

    def __str__(self):
        return self.get_full_name() or self.get_short_name() or self.phone


class UserAddress(Address):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", verbose_name=_("user"))
    label = models.CharField(verbose_name=_("label"), max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    is_default = models.BooleanField(verbose_name=_("is_default"),
                                     default=False)  # todo: each user should only have ONE default address

    objects = SoftDeleteManager()

    class Meta:
        verbose_name = _("user address")
        verbose_name_plural = _("user addresses")

    def set_default(self):
        if default_address := self.user.addresses.filter(is_default=True).first():
            if default_address.id != self.id:
                default_address.is_default = False
                default_address.save()

    def soft_delete(self):
        self.is_deleted = True
        self.is_default = False
        self.save()

    def delete(self, *args, soft_delete=False, **kwargs):
        if soft_delete:
            self.soft_delete()
        else:
            super().delete(*args, *kwargs)

    def save(self, *args, **kwargs):
        if self.is_default:
            self.set_default()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.label or super().__str__()
