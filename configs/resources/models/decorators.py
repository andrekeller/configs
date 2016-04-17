"""
confi.gs resources model decorators
"""
from cidrfield import IPv4Network
from cidrfield import IPv6Network


def valid_network_property(method):
    """
    Ensures that the NetworkModel has a valid network field.
    """
    def wrapper(self):
        if not self.network:
            return None
        if not isinstance(self.network, (IPv4Network, IPv6Network)):
            return None
        return method(self)
    return property(wrapper)

