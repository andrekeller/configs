"""
confi.gs cidrfield tests for __init__.py
"""
# django
from django.test import TestCase
# confi.gs
from cidrfield import IPv4Network, IPv6Network


class IPNetworkTestCase(TestCase):

    def test_ipnetwork_network_prefixlen(self):

        network_v4 = IPv4Network('203.0.113.128/27')
        network_v6 = IPv6Network('2001:db8:cafe::/64')

        self.assertEqual(str(network_v4), '203.0.113.128/27')
        self.assertEqual(str(network_v6), '2001:db8:cafe::/64')

    def test_ipnetwork_host_prefixlen(self):

        network_v4 = IPv4Network('203.0.113.128/32')
        network_v6 = IPv6Network('2001:db8:cafe::/128')

        self.assertEqual(str(network_v4), '203.0.113.128')
        self.assertEqual(str(network_v6), '2001:db8:cafe::')
