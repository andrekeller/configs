"""
confi.gs cidrfield tests for validators.py
"""
# django
from django.core.exceptions import ValidationError
from django.test import TestCase
# confi.gs
from cidrfield import IPv4Network, IPv6Network
from cidrfield.validators import validate_network


class ValidateNetworkTestCase(TestCase):

    def test_validate_valid_ipnetwork(self):
        ipv4 = IPv4Network('203.0.113.16/29')
        ipv4_str = '203.0.113.16/29'
        ipv6 = IPv6Network('2001:db8:1234:5678::/64')
        ipv6_str = '2001:db8:1234:5678::/64'

        self.assertEqual(ipv4, validate_network(ipv4))
        self.assertEqual(ipv4, validate_network(ipv4_str))
        self.assertEqual(ipv6, validate_network(ipv6))
        self.assertEqual(ipv6, validate_network(ipv6_str))

    def test_validate_invalid_ipnetwork(self):
        no_ipv4 = 'test123'
        ipv4_wrong_address = '203.0.313.16/29'
        ipv4_wrong_netmask = '203.0.113.16/35'
        no_ipv6 = 'test456'
        ipv6_wrong_address = '2001:dg8:1234:5678::/64'
        ipv6_wrong_netmask = '2001:db8:1234:5678::/135'

        with self.assertRaises(ValidationError):
            _ = validate_network(no_ipv4)
        with self.assertRaises(ValidationError):
            _ = validate_network(ipv4_wrong_address)
        with self.assertRaises(ValidationError):
            _ = validate_network(ipv4_wrong_netmask)
        with self.assertRaises(ValidationError):
            _ = validate_network(no_ipv6)
        with self.assertRaises(ValidationError):
            _ = validate_network(ipv6_wrong_address)
        with self.assertRaises(ValidationError):
            _ = validate_network(ipv6_wrong_netmask)

