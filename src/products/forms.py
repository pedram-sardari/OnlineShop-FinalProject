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
        super().__init__(*args, **kwargs)
        # self.fields.appent()

    # colors = forms.ModelMultipleChoiceField()

    class Meta:
        model = ProductColor
        fields = ['color']


class RatingForm(FormatFormFieldsMixin, forms.ModelForm):
    score = forms.ChoiceField(label=_("امتیاز"), choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])

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
            # if self.instance and self.instance.store_discount:
            #     self.fields['store_discount'].initial = StoreDiscount.objects.get(id=self.instance.store_discount.id)
        if self.store:
            # if self.instance and self.instance.product_color:
            #     self.fields['product_color'].initial = ProductColor.objects.get(id=self.instance.store_discount.id)
            self.fields['product_color'].queryset = ProductColor.objects.filter(product=self.product)
        self.format_fields()

