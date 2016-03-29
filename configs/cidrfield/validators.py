from ipaddress import AddressValueError, NetmaskValueError
from django.core.exceptions import ValidationError
from . import IPv4Network, IPv6Network


def validate_network(value):
    if isinstance(value, (IPv4Network, IPv6Network)):
        return value

    try:
        return IPv4Network(value, strict=True)
    except (AddressValueError, NetmaskValueError):
        pass
    try:
        return IPv6Network(value, strict=True)
    except (AddressValueError, NetmaskValueError):
        pass
    raise ValidationError('%r does not appear to be an IPv4 or IPv6 network' %
                          value)
