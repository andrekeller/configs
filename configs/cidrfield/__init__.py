"""
configs cidr field.

django model field that implements the PostgreSQL CIDR field.
"""
import ipaddress


class IPv4Network(ipaddress.IPv4Network):
    """
    Represents an IPv4 network
    """

    def __str__(self):
        """
        Returns a string representation of the ipv4 network prefix.
        """
        if self.prefixlen == self.max_prefixlen:
            return str(self.network_address)
        return '%s/%d' % (self.network_address, self.prefixlen)


class IPv6Network(ipaddress.IPv6Network):
    """
    Represents an IPv6 network
    """

    def __str__(self):
        """
        Returns a string representation of the ipv6 network prefix.
        """
        if self.prefixlen == self.max_prefixlen:
            return str(self.network_address)
        return '%s/%d' % (self.network_address, self.prefixlen)
