# App_History/templatetags/group_permissions.py
from django import template

register = template.Library()

@register.filter
def has_group(user, group_list):
    if not hasattr(user, 'user_group'):
        return False
    return user.user_group.user_group_type in group_list
