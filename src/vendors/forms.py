from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.forms import RegisterEmailForm
from orders.models import OrderItem
from products.models import Product
from website.forms import FormatFormFieldsMixin
from website.models import Address
from .models import Owner, Store, Staff


class OwnerRegisterEmailForm(RegisterEmailForm):
    class Meta:
        model = Owner
        fields = ['email']


class StoreForm(FormatFormFieldsMixin, forms.ModelForm):
    store_name = forms.CharField(label=_("نام فروشگاه"), max_length=100)

    class Meta:
        model = Address
        fields = ['store_name', 'province', 'city', 'neighborhood', 'street', 'alley', 'no', 'zipcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()

    def clean_store_name(self):
        store_name = self.cleaned_data.get('store_name')
        old_store = Store.objects.filter(name=store_name).first()
        # self.instance == new_store
        if old_store and self.instance and old_store.id != self.instance.id:
            raise forms.ValidationError(_(f"«{store_name}» قبلا ثبت شده است. "))
        return store_name


class StaffRegistrationForm(FormatFormFieldsMixin, BaseUserCreationForm):
    role = forms.ChoiceField(label=_("عنوان شغلی"), choices=Staff.Roles.choices[1:])

    class Meta:
        model = Staff
        fields = ['email', 'role', 'password1', 'password2', 'gender', 'first_name', 'last_name', 'national_id',
                  'date_of_birth', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class StaffUpdateForm(FormatFormFieldsMixin, forms.ModelForm):
    role = forms.ChoiceField(label=_("عنوان شغلی"), choices=Staff.Roles.choices[1:])

    class Meta:
        model = Staff
        fields = ['email', 'role', 'gender', 'first_name', 'last_name', 'national_id',
                  'date_of_birth', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class OrderItemStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['status']


class ProductForm(FormatFormFieldsMixin, forms.ModelForm):
    image1 = forms.ImageField()

    class Meta:
        model = Product
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'files'):
            for field, img in self.files.items():
                self.fields[field] = forms.ImageField(required=False)
        self.format_fields()
