from django import forms


class FormatFormFieldsMixin:
    def format_fields(self):
        for field in self.fields.values():  # NOQA
            if isinstance(field, forms.DateField) or isinstance(field, forms.DateTimeField):
                field.widget.input_type = 'date'

            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field, forms.ChoiceField):
                field.widget.attrs.update({'class': 'form-select form-select-lg mb-3'})
            else:
                field.widget.attrs.update({'class': 'form-control form-control-lg'})
