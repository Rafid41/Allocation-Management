# templatetags/custom_filters.py

from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def replace_underscore(value):
    if value:
        return str(value).replace('_', ' ').title()
    return value
