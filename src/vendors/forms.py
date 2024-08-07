from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Owner, Store
from website.models import Address, CITIES, PROVINCES


class OwnerRegisterForm(UserCreationForm):
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

    def clean_store_name(self):
        store_name = self.cleaned_data.get('store_name')
        if Store.objects.filter(name=store_name).exists():
            # raise forms.ValidationError(_(f"'{store_name}' قبلا ثبت شده است. رستوران با نام "))
            raise forms.ValidationError(_(f"«{store_name}» قبلا ثبت شده است. "))
        return store_name
