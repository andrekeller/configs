"""
confi.gs cidrfield.

django model field that implements the PostgreSQL CIDR field.
"""
import ipaddress


class IPNetworkMixin:
    """
    Mixin to change the representation of an ipaddress.IPv4Network or
    ipaddress.IPv6Network to exclude prefixlen for host addresses.
    """

    def __str__(self):
        """
        Returns a string representation of the network prefix,
        without prefixlen if network prefix is a host address.
        """
        if self.prefixlen == self.max_prefixlen:
            return str(self.network_address)
        return '%s/%d' % (self.network_address, self.prefixlen)


class IPv4Network(IPNetworkMixin, ipaddress.IPv4Network):
    """
    Represents an IPv4 network
    """


class IPv6Network(IPNetworkMixin, ipaddress.IPv6Network):
    """
    Represents an IPv6 network
    """
