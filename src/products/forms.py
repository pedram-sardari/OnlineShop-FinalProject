from django.utils import timezone

from django import forms
from django.utils.translation import gettext_lazy as _

from website.forms import FormatFormFieldsMixin
from .models import Comment, Rating, ProductColor, Product, StoreProduct, StoreDiscount


class CommentForm(FormatFormFieldsMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class ProductColorForm(FormatFormFieldsMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        qs = ProductColor.objects.filter(product=product)
        self.fields['color'].queryset = qs
        self.fields['color'].initial = qs.first()

    # colors = forms.ModelMultipleChoiceField()

    class Meta:
        model = ProductColor
        fields = ['color']


class RatingForm(FormatFormFieldsMixin, forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class StoreDiscountForm(FormatFormFieldsMixin, forms.ModelForm):
    class Meta:
        model = StoreDiscount
        fields = ['cash_discount', 'percentage_discount', 'expiration_date', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()

    def clean(self):
        cleaned_data = super().clean()
        cash_discount = cleaned_data.get("cash_discount")
        percentage_discount = cleaned_data.get("percentage_discount")
        if not (cash_discount or percentage_discount):
            raise forms.ValidationError("Please provide one of cash_discount or percentage_discount.")
        if cash_discount and percentage_discount:
            raise forms.ValidationError("Please provide only one of cash_discount or percentage_discount.")

        if cash_discount is None:
            cleaned_data['cash_discount'] = 0
        if percentage_discount is None:
            cleaned_data['percentage_discount'] = 0
        return cleaned_data

    def clean_percentage_discount(self):
        cash_discount = self.cleaned_data.get("cash_discount")
        percentage_discount = self.cleaned_data.get("percentage_discount")
        if not cash_discount and percentage_discount and (percentage_discount > 100 or percentage_discount < 1):
            raise forms.ValidationError("Percentage must be between 0 and 100.")
        return percentage_discount

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get("expiration_date")
        if expiration_date < timezone.now():
            raise forms.ValidationError("The expiration date must be after the current date.")
        return expiration_date


class SelectProductForm(FormatFormFieldsMixin, forms.Form):
    product = forms.ModelChoiceField(label=_("محصول مورد نظر"), queryset=Product.objects.filter(is_available=True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_fields()


class StoreProductForm(FormatFormFieldsMixin, forms.ModelForm):
    class Meta:
        model = StoreProduct
        fields = ['price', 'inventory', 'product_color', 'store_discount', 'is_available']

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        self.store = kwargs.pop('store', None)
        super().__init__(*args, **kwargs)

        # Fill the `select` tag with corresponding data
        if self.product:
            self.fields['store_discount'].queryset = StoreDiscount.objects.filter(store=self.store)
        if self.store:
            self.fields['product_color'].queryset = ProductColor.objects.filter(product=self.product)
        self.format_fields()

    def clean_store_discount(self):
        price = self.cleaned_data.get('price')
        store_discount = self.cleaned_data.get('store_discount')
        if store_discount and store_discount.get_discounted_price(price) < 0:
            raise forms.ValidationError('Discount is greater than the price!')
        return store_discount
