from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Customer
from website.forms import CustomModeForm


class CustomerRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field, forms.DateField):
                field.widget.attrs.update(
                    {
                        'type': 'date'
                    }
                )
                field.widget.input_type = 'date'
            field.widget.attrs.update(
                {
                    'class': 'form-control form-control-lg',
                }
            )
    class Meta:
        model = Customer
        fields = ['email']


class CustomerChangeForm(CustomModeForm):


    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'national_id', 'gender', 'date_of_birth', 'image', ]
