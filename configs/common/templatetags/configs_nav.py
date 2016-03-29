"""
configs template tags
"""
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def navactive(context, url):
    """
    returns active if the current request url matches the beginning of a
    supplied url.
    """
    request = context['request']
    if request.path.startswith(reverse(url)):
        return "active"
    return ""

