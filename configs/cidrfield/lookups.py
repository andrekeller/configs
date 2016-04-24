"""
confi.gs lookups for cidrfield.
"""
# stdlib
import ipaddress
# django
from django.db.models import Lookup


class NetContains(Lookup):
    """
    lookup to find parent networks
    """
    lookup_name = 'contains'

    def as_sql(self, qn, connection):
        # TODO: add test
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs = ipaddress.ip_network(self.rhs, strict=False)
        return "%s >> '%s'" % (lhs, rhs), lhs_params


class NetContained(Lookup):
    """
    lookup to find child networks
    """
    lookup_name = 'contained'

    def as_sql(self, qn, connection):
        # TODO: add test
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs = ipaddress.ip_network(self.rhs, strict=False)
        return "%s << '%s'" % (lhs, rhs), lhs_params
