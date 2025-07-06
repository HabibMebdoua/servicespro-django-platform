# accounts/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def has_deliveryperson(user):
    return hasattr(user, 'deliveryperson')