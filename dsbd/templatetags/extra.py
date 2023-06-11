from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def to_int(value):
    if not value:
        return None
    return int(value)


@register.simple_tag
def beta():
    return settings.BETA


@register.simple_tag
def debug():
    return settings.DEBUG
