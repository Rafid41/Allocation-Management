# App_Status\templatetags\status_custom_filters.py
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
