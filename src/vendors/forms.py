from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm

from .models import Owner, Store, Manager, Operator, Staff
from website.models import Address, CITIES, PROVINCES
from website.forms import FormatFormFieldsMixin


class OwnerRegistrationForm(FormatFormFieldsMixin, BaseUserCreationForm):
    store_name = forms.CharField(label=_("نام فروشگاه"), max_length=100)
    province = forms.ChoiceField(label=_("استان"), choices=PROVINCES)
    city = forms.ChoiceField(label=_("شهر"), choices=CITIES)
    neighborhood = forms.CharField(label=_("محله"), max_length=100, required=False)
    street = forms.CharField(label=_("خیابان"), max_length=100, required=False)
    alley = forms.CharField(label=_("کوچه"), max_length=100, required=False)
    no = forms.CharField(label=_("پلاک"), max_length=100, required=False)
    zipcode = forms.CharField(label=_("کد پستی"), max_length=100, required=False)

    class Meta:
        model = Owner
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()

    def clean_store_name(self):
        store_name = self.cleaned_data.get('store_name')
        if Store.objects.filter(name=store_name).exists():
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
