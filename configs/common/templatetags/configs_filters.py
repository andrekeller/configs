"""
confi.gs template filters.
"""
# stdlib
from urllib.parse import urlencode
# django
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter()
def first_line(value):
    """
    returns first line of a multiline input.
    """
    if not value:
        return ''

    return value.splitlines()[0]


@register.filter()
def prefix_help(value, family=4):
    """
    returns a help text based on the prefixlen and address family.
    """
    if family == 4:
        return " (%d addresses)" % (2 ** (32 - value))
    else:
        if value == 127:
            return " (2 addresses)"
        elif value == 126:
            return " (4 addresses)"
        elif value == 64:
            return " network"
        elif 47 < value < 64:
            return " (%d /64 networks)" % (2 ** (64 - value))
        elif value < 48:
            return " (%d /48 networks)" % (2 ** (48 - value))
    return ""


@register.filter()
def percentage(value):
    """
    returns the input as a single decimal rounded %-sign suffixed value
    """
    if not value:
        return '0%'

    return "%.1f%%" % value


@register.filter()
def add_class(field, class_name):
    """
    adds a css class to a django form widget
    """
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
    })


@register.simple_tag()
def api_url(resource, **kwargs):
    """
    returns the api_url for a specific resource resource
    """
    resource_url = reverse('api_dispatch_list',
                           kwargs={'resource_name': resource, 'api_name': 'v1'})
    if kwargs:
        return resource_url + '?' + urlencode(kwargs)
    return resource_url

