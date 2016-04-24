"""
confi.gs navigation template tags
"""
from django import template
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def navactive(context, url):
    """
    returns active if the current request url matches the beginning of a
    supplied url.
    """
    # TODO: add test
    request = context['request']
    if request.path.startswith(reverse(url)):
        return "active"
    return ""


@register.simple_tag(takes_context=True)
def navactive_namespace(context, namespace):
    """
    returns active if the current request url is
    supplied url.
    """
    # TODO: add test
    request = context['request']
    if resolve(request.path).namespace == namespace:
        return "active"
    return ""
