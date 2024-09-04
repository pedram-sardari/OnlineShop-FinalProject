from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm, PasswordChangeForm
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
        fields = ['first_name', 'last_name', 'national_id', 'gender', 'date_of_birth', 'image', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class EmailAndPasswordChangeForm(FormatFormFieldsMixin, PasswordChangeForm):
    email = forms.EmailField()

    def __init__(self, user, *args, **kwargs):
        """The `user` argument is required"""
        super().__init__(user, *args, **kwargs)
        self.format_fields()

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user and self.user.email != user.email:
            raise forms.ValidationError('Email already registered!')
        return email

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
        return self.user


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
    phone = forms.CharField(max_length=11, label=_("phone number"), validators=[phone_validator])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class LoginPhoneForm(PhoneForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop('request', None)  # LoginView passes request to this form inside the LoginPhone
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Try to retrieve the user associated with the session phone number
        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_("You haven't register"))
        return phone


class RegisterPhoneForm(PhoneForm):
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('This phone number is already registered.'))
        return phone


class UpdatePhoneForm(PhoneForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = User.objects.filter(phone=phone).first()
        if user and user.phone != self.user.phone:
            raise forms.ValidationError(_('This phone number is already registered.'))
        return phone


class OTPForm(FormatFormFieldsMixin, forms.Form):
    otp = forms.CharField(max_length=settings.OTP_LENGTH, label=_("verification code"))

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
            raise forms.ValidationError(_('The verification code has expired.'))

        # If the provided OTP does not match the session OTP
        if user_otp != session_otp:
            raise forms.ValidationError(_('The verification code is incorrect'))
        return user_otp
