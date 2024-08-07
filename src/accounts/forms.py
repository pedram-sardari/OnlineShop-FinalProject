from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(AuthenticationForm):
    # class Meta:
    #     model = User
    #     fields = ('username', 'password')
    #     widgets = {
    #         'password': forms.PasswordInput
    #     }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control form-control-lg',
                'id': 'username'
            }
        )

        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control form-control-lg',
                'id': 'password'
            }
        )
