"""
confi.gs cidrfield validators
"""
# stdlib
from ipaddress import AddressValueError
from ipaddress import NetmaskValueError
# django
from django.core.exceptions import ValidationError
# confi.gs
from . import IPv4Network
from . import IPv6Network


def validate_network(network_string):
    """
    validate if a string represents a valid network address

    :param network_string: network address to validate
    :return: IPv4Network or IPv6Network, depending on the input.
    :raises: ValidationError if the address is invalid
    """
    if isinstance(network_string, (IPv4Network, IPv6Network)):
        return network_string

    try:
        return IPv4Network(network_string, strict=True)
    except (AddressValueError, NetmaskValueError):
        pass
    try:
        return IPv6Network(network_string, strict=True)
    except (AddressValueError, NetmaskValueError):
        pass
    raise ValidationError('%r does not appear to be an IPv4 or IPv6 network' %
                          network_string)
