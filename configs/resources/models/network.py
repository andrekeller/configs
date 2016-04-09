"""
configs resources app network model
"""

from collections import deque
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import connection, models
from tagging.fields import TagField
from cidrfield.fields import CidrField
from cidrfield.validators import validate_network
from cidrfield import IPv4Network, IPv6Network
from .decorators import valid_network_property


class RootNetworkManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().extra(
            where=["""
                NOT EXISTS(
                    SELECT n.network
                    FROM resources_network n
                    WHERE
                        n.network >> "resources_network"."network" AND
                        n.vrf_id = "resources_network"."vrf_id"
                )"""""]
        )



class Network(models.Model):
    """
    model to represent the networks and ip addresses.
    """
    network = CidrField(validators=[validate_network, ])
    description = models.TextField(null=True, blank=True)
    vrf = models.ForeignKey('resources.Vrf', default=1)
    vlan = models.ForeignKey('resources.Vlan', blank=True, null=True)
    use_reserved_addresses = models.BooleanField(default=False)
    status = models.ForeignKey('resources.ResourceStatus', default=1)
    tags = TagField()
    host = models.ForeignKey('resources.Host', blank=True, null=True)

    objects = models.Manager()
    root_objects = RootNetworkManager()

    class Meta:
        ordering = ['network']
        unique_together = ("network", "vrf")

    def __str__(self):
        """
        string representation of network objects

        :returns: network in cidr notation. if /32 (or /128 if IPv6) the
                  prefix length is omitted.
        :rtype: str
        """
        return str(self.network)

    @valid_network_property
    def child_blocks(self):
        """
        child blocks of the network object.

        :returns: child blocks
        :rtype: RawQuerySet
        """
        return Network.objects.extra(
            where=["""
                "resources_network"."network" << %s AND
                "resources_network"."vrf_id" = %s AND
                NOT EXISTS  (
                    SELECT 1
                    FROM resources_network n
                    WHERE
                        "resources_network"."network" << n.network AND
                         n.network << %s
                )
            """],
            params=(self.network.compressed, self.vrf_id, self.network.compressed)
        ).order_by('network')

    @valid_network_property
    def netmask(self):
        return self.network.netmask

    @valid_network_property
    def network_address(self):
        """
        network address (network id, host-part of address all zero) of the
        network object.

        :returns: network address (network id)
        :rtype: str
        """
        return str(self.network.network_address)

    @valid_network_property
    def broadcast_address(self):
        """
        broadcast address (host-part of address all one) of the network object.

        :returns: broadcast address
        :rtype: str
        """
        return str(self.network.broadcast_address)

    @valid_network_property
    def host_max(self):
        if self.use_reserved_addresses or self.family == 6:
            return self.network.broadcast_address
        return self.network.broadcast_address - 1

    @valid_network_property
    def host_min(self):
        if self.use_reserved_addresses:
            return self.network.network_address
        return self.network.network_address + 1

    @valid_network_property
    def is_host(self):
        return self.network.prefixlen == self.network.max_prefixlen

    @valid_network_property
    def family(self):
        """
        address family of the network object.

        :returns: address family
        :rtype: int
        """
        return self.network.version

    @valid_network_property
    def num_addresses(self):
        """
        number of usable addresses in the network object.

        :returns: number of usable addresses
        :rtype: int
        """
        if self.use_reserved_addresses:
            return self.network.num_addresses

        if self.family == 4:
            # ipv4 and reserverd addresses are not allowed, so substract
            # network and broadcast address
            return self.network.num_addresses - 2
        if self.family == 6:
            # ipv6 and reserverd addresses are not allowed, so substract
            # network address
            return self.network.num_addresses - 1

    @property
    def parent_block(self):
        """
        most specific parent block of network object.

        :returns: Network
        """
        try:
            return self.parent_blocks[0]
        except IndexError:
            return None

    @property
    def parent_blocks(self):
        """
        parent blocks of network object.

        :returns: QuerySet
        """
        return Network.objects.filter(
            network__contains='%s' % self.network,
            vrf_id=self.vrf_id
        ).order_by('-network')

    def next(self, prefixlen=32):
        if not self.network:
            return None
        if not isinstance(self.network, (IPv4Network, IPv6Network)):
            return None

        cursor = connection.cursor()
        cursor.execute('''
          SELECT find_free_block(%(vrf)s, %(parent)s, %(prefixlen)s)
        ''', {'vrf': self.vrf_id,
              'parent': self.network.compressed,
              'prefixlen': prefixlen})
        try:
            return validate_network(cursor.fetchone()[0])
        except ValidationError:
            return None

    @valid_network_property
    def prefixlens(self):
        """
        "sane" prefixlens for child blocks within this network
        :return: list of prefixlen
        """
        if self.family == 4:
            prefixlens = deque(range(self.prefixlen + 1, 32))
        else:
            prefixlens = deque(range(self.prefixlen + 1, 65))
            prefixlens.append(127)

        for prefixlen in prefixlens.copy():
            if self.next(prefixlen):
                return prefixlens
            prefixlens.popleft()

        return prefixlens

    @valid_network_property
    def assigned(self):
        """
        percentage of assigned addresses in relation to available addresses

        :return: percentage of addresses
        :rtype: float
        """
        cursor = connection.cursor()
        cursor.execute('''
          SELECT COUNT(*)
          FROM   resources_network c
          WHERE  c.network << %(network)s AND c.vrf_id = %(vrf_id)s
          AND    masklen(c.network) = %(max_prefixlen)s
          AND    NOT EXISTS(
            SELECT 1
            FROM   resources_network n
            WHERE  c.network << n.network AND n.network << %(network)s
          )
        ''', {'max_prefixlen': self.network.max_prefixlen,
              'network': self.network.compressed,
              'vrf_id': self.vrf_id})

        try:
            return cursor.fetchone()[0] * 100 / self.num_addresses
        except ZeroDivisionError:
            return 100
        except (ValueError, TypeError):
            return None

    @valid_network_property
    def allocated(self):
        """
        percentage of suballocated addresses in relation to available addresses

        :return: percentage of addresses
        :rtype: float
        """
        cursor = connection.cursor()
        cursor.execute('''
          SELECT DISTINCT SUM(2 ^ (%(max_prefixlen)s - masklen(c.network)))
          FROM   resources_network c
          WHERE  c.network << %(network)s AND c.vrf_id = %(vrf_id)s
          AND    masklen(c.network) < %(max_prefixlen)s
          AND    NOT EXISTS(
            SELECT 1
            FROM   resources_network n
            WHERE  c.network << n.network AND n.network << %(network)s
          )
        ''', {'max_prefixlen': self.network.max_prefixlen,
              'network': self.network.compressed,
              'vrf_id': self.vrf_id})

        try:
            return cursor.fetchone()[0] * 100 / self.network.num_addresses
        except (ValueError, TypeError):
            return 0.0

    @valid_network_property
    def prefixlen(self):
        """
        cidr prefix length in bits

        :returns: cidr prefix length
        :rtype: int
        """
        return self.network.prefixlen

    @valid_network_property
    def max_prefixlen(self):
        """
        cidr max prefix length in bits

        :returns: cidr max prefix length for networks address family
        :rtype: int
        """
        return self.network.max_prefixlen

    def get_absolute_url(self):
        """
        canonical url for network object

        :returns: url
        :rtype: str
        """
        return reverse('resources:network-detail', args=[self.pk])

    def clean(self):
        cleaned_data = super(Network, self).clean()

        if self.network is None:
            return None

        try:
            validate_network(self.network)
        except ValidationError:
            return None

        if self.vlan:
            if not self.vrf_id == self.vlan.vrf_id:
                raise ValidationError('VRF of network and VLAN must match')
        if self.parent_block and self.prefixlen == self.network.max_prefixlen:
            if not self.parent_block.use_reserved_addresses:
                if self.parent_block.network_address == str(self.network):
                    raise ValidationError('network address')
                if self.family == 4:
                    if self.parent_block.broadcast_address == str(self.network):
                        raise ValidationError('broadcast address')

        if self.prefixlen < self.network.max_prefixlen:
            if not self.use_reserved_addresses:
                try:
                    if self.network_address == str(
                        self.child_blocks.first()
                    ):
                        raise ValidationError('network address')
                except IndexError:
                    pass

                if self.family == 4:
                    try:
                        if self.broadcast_address == str(
                                self.child_blocks.order_by('-network').first()
                        ):
                            raise ValidationError('broadcast address')
                    except IndexError:
                        pass

        return cleaned_data

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance
