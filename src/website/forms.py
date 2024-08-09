from django import forms


class CustomModeForm(forms.ModelForm):
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


import jdatetime


class JalaliDateInput(forms.DateInput):
    input_type = 'date'

    def format_value(self, value):
        if value is None:
            return ''
        if isinstance(value, jdatetime.date):
            return value.strftime('%Y-%m-%d')
        return super().format_value(value)


class JalaliDateField(forms.DateField):
    widget = JalaliDateInput

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            dt = jdatetime.date.strptime(value, '%Y-%m-%d')
            return dt.togregorian().date()
        except ValueError:
            raise forms.ValidationError('Invalid date format')


class JalaliDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

    def format_value(self, value):
        if value is None:
            return ''
        if isinstance(value, jdatetime.datetime):
            return value.strftime('%Y-%m-%dT%H:%M:%S')
        return super().format_value(value)


class JalaliDateTimeField(forms.DateTimeField):
    widget = JalaliDateTimeInput

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            dt = jdatetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            return dt.togregorian()
        except ValueError:
            raise forms.ValidationError('Invalid date format')
