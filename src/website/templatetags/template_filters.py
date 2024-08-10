from django import template

register = template.Library()


@register.filter
def default_if_none(value, default_value="-"):
    if not value:
        return default_value
    return value


@register.filter
def slice_string(value, length=15):
    if not isinstance(value, str):
        raise ValueError('slice string not supported')
    if len(value) > length:
        return value[:length - 3] + '...'
    return value
