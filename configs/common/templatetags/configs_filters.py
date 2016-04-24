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

    try:
        return value.splitlines()[0]
    except AttributeError:
        raise ValueError('first_line filter needs a string as value')


@register.filter()
def prefix_help(value, family=4):
    """
    returns a help text based on the prefixlen and address family.
    """
    try:
        if family == 4:
            if not 1 <= value <= 31:
                raise ValueError('IPv4 prefixlen needs to be between 0 and 32')
            return " (%d addresses)" % (2 ** (32 - value))
        elif family == 6:
            if not 1 <= value <= 127:
                raise ValueError('IPv6 prefixlen needs to be between 0 and 128')
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
            else:
                return ""
        else:
            raise ValueError("family needs to be either 4 or 6")
    except TypeError:
        raise ValueError("prefixlen needs to be an integer")


@register.filter()
def percentage(value):
    """
    returns the input as a single decimal rounded %-sign suffixed value
    """
    if not value:
        return '0%'

    try:
        return "%.1f%%" % value
    except TypeError:
        raise ValueError('percentage filter needs a float as value')


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

