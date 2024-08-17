from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

phone_validator = RegexValidator(
    regex="^(\\+98|0)?9\\d{9}$", message=_("Invalid phone number!")
)  # TODO: proper message
