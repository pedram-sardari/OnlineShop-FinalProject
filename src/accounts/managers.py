from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, email, phone, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not (email or phone):
            raise ValueError(_("Either email or phone must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, phone, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
