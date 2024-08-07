from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Customer


class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email']
