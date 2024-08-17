from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import UserAddress
from website.forms import FormatFormFieldsMixin
from website.validators import phone_validator

User = get_user_model()


class LoginForm(FormatFormFieldsMixin, AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class MyUserChangeForm(FormatFormFieldsMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'national_id', 'gender', 'date_of_birth', 'image', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class UserAddressForm(FormatFormFieldsMixin, forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ('user', 'is_deleted')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class RegisterEmailForm(FormatFormFieldsMixin, BaseUserCreationForm):
    """Be sure to define a `Meta` class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class PhoneForm(FormatFormFieldsMixin, forms.Form):
    phone = forms.CharField(max_length=11, label=_("شماره تماس"), validators=[phone_validator])

    def __init__(self, *args, **kwargs):
        kwargs.pop('request', None)  # LoginView passes request to this form inside the LoginPhone
        super().__init__(*args, **kwargs)
        self.format_fields()


class LoginPhoneForm(PhoneForm):
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Try to retrieve the user associated with the session phone number
        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('شما ثبتنام نکرده اید')
        return phone


class RegisterPhoneForm(PhoneForm):
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('این شماره تماس قبلا ثبت شده است.')
        return phone


class OTPForm(FormatFormFieldsMixin, forms.Form):
    otp = forms.CharField(max_length=settings.OTP_LENGTH, label="کد تایید")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.format_fields()

    def clean_otp(self):
        user_otp = self.cleaned_data['otp']
        session_otp = self.request.session.get('otp')
        print('*' * 50, user_otp, session_otp)

        # If OTP session is missing or expired, redirect back to login
        if not session_otp:
            raise forms.ValidationError('کد تایید منقضی شده است')

        # If the provided OTP does not match the session OTP
        if user_otp != session_otp:
            raise forms.ValidationError('کد تایید اشتباه است')
        return user_otp
