from django import template
from babel.numbers import format_decimal

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


@register.filter(name='format_number')
def format_number(value, locale='fa'):
    """Format a number according to the locale."""
    try:
        return format_decimal(value, locale=locale)
    except (TypeError, ValueError):
        return value
