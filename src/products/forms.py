from django import forms
from django.utils.translation import gettext_lazy as _

from website.forms import FormatFormFieldsMixin
from .models import Comment, Rating, ProductColor


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
