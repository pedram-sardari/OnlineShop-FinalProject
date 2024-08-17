from django import forms

from accounts.forms import RegisterEmailForm
from website.forms import FormatFormFieldsMixin
from .models import Customer


class CustomerRegisterForm(RegisterEmailForm):
    class Meta:
        model = Customer
        fields = ['email']


class CustomerChangeForm(FormatFormFieldsMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'national_id', 'gender', 'date_of_birth', 'image', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()
