from django import template

register = template.Library()

@register.filter
def capitalize(value):
    return value.upper() if isinstance(value, str) else None
