from django import template
from django.conf import settings
import datetime
import markdown as md

register = template.Library()


@register.simple_tag
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.simple_tag
def url_replace(request, **kwargs):
    params = request.GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    return params.urlencode()


@register.simple_tag
def time_to_str(gmt):
    if gmt is None:
        return "無期限"
    jst = gmt + datetime.timedelta(hours=0)
    if not gmt:
        return "取得失敗"
    return jst.strftime("%Y/%m/%d %H:%M")


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
