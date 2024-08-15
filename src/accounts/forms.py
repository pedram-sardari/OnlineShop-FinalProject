from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import UserAddress
from website.forms import FormatFormFieldsMixin

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


class PhoneForm(FormatFormFieldsMixin, forms.Form):
    phone = forms.CharField(max_length=11)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class VerificationCodeForm(FormatFormFieldsMixin, forms.Form):
    verification_code = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()
