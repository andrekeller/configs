from cidrfield import IPv4Network, IPv6Network


def valid_network_property(method):
    def wrapper(self):
        if not self.network:
            return None
        if not isinstance(self.network, (IPv4Network, IPv6Network)):
            return None
        return method(self)
    return property(wrapper)

