"""
confi.gs resources network models
"""
# stdlib
from collections import deque
# django
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import connection
from django.db import models
# 3rd-party
from tagging.fields import TagField
# confi.gs
from cidrfield import IPv4Network
from cidrfield import IPv6Network
from cidrfield.fields import CidrField
from cidrfield.validators import validate_network
from .decorators import valid_network_property


class NetworkManager(models.Manager):
    """
    Default manager for the network model
    """

    def search(self, term):
        pass


class HostNetworkManager(models.Manager):
    """
    Manager for the network model, returning only host addresses.
    """

    def get_queryset(self):
        """
        Returns a QuerySet, containing only host addresses.
        (i.e. /128 prefixes for IPv6, /32 prefixes for IPv4)
        """
        return super().get_queryset().extra(
            where=["""
              (masklen(network) = 32 AND family(network) = 4) OR
              (masklen(network) = 128 AND family(network) = 6)
            """]
        )


class RootNetworkManager(models.Manager):
    """
    Manager for the network model, returning only root (parent-less) networks.
    """

    def get_queryset(self):
        """
        Returns QuerySet, containing only prefixes without parent.
        """
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
    confi.gs network model
    """
    network = CidrField(validators=[validate_network, ])
    description = models.TextField(null=True, blank=True)
    vrf = models.ForeignKey('resources.Vrf', default=1)
    vlan = models.ForeignKey('resources.Vlan', blank=True, null=True)
    use_reserved_addresses = models.BooleanField(default=False)
    status = models.ForeignKey('resources.ResourceStatus', default=1)
    tags = TagField()
    host = models.ForeignKey('resources.Host', blank=True, null=True)

    objects = NetworkManager()
    root_objects = RootNetworkManager()
    host_objects = HostNetworkManager()

    class Meta:
        ordering = ['network']
        unique_together = ("network", "vrf")

    def __str__(self):
        """
        string representation of network objects
        """
        return str(self.network)

    @valid_network_property
    def child_blocks(self):
        """
        returns child blocks of the network object as a QuerySet.
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
        """
        returns netmask of the network object
        """
        return self.network.netmask

    @valid_network_property
    def network_address(self):
        """
        returns network address (network id, host-part of address all zero) of the
        network object.
        """
        return str(self.network.network_address)

    @valid_network_property
    def broadcast_address(self):
        """
        returns broadcast address (host-part of address all one) of the network object.
        """
        return str(self.network.broadcast_address)

    @valid_network_property
    def host_max(self):
        """
        returns last usable address of the network object.
        """
        if self.use_reserved_addresses or self.family == 6:
            return self.network.broadcast_address
        return self.network.broadcast_address - 1

    @valid_network_property
    def host_min(self):
        """
        returns first usable address of the network object.
        """
        if self.use_reserved_addresses:
            return self.network.network_address
        return self.network.network_address + 1

    @valid_network_property
    def is_host(self):
        return self.network.prefixlen == self.network.max_prefixlen

    @valid_network_property
    def family(self):
        """
        returns address family of the network object as int.
        """
        return self.network.version

    @valid_network_property
    def num_addresses(self):
        """
        returns number of usable addresses in the network object.
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
        returns most specific parent block of network object as network object.
        """
        try:
            return self.parent_blocks[0]
        except IndexError:
            return None

    @property
    def parent_blocks(self):
        """
        returns all parent blocks of network object as QuerySet.
        """
        return Network.objects.filter(
            network__contains='%s' % self.network,
            vrf_id=self.vrf_id
        ).order_by('-network')

    def next(self, prefixlen=32):
        """
        returns next free prefix within network object.
        """
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
        """
        # todo: this should be an annotation in the default QuerySet
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
        """
        # todo: this should be an annotation in the default QuerySet
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
        returns cidr prefix length of the network object as int
        """
        return self.network.prefixlen

    @valid_network_property
    def max_prefixlen(self):
        """
        returns cidr max prefix length of the network objects family as int
        """
        return self.network.max_prefixlen

    def get_absolute_url(self):
        """
        returns a canonical url for network object
        """
        return reverse('resources:network-detail', args=[self.pk])

    def clean(self):
        """
        returns a validated data of the network object
        """
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
                    # todo: better error message
                    raise ValidationError('network address')
                if self.family == 4:
                    if self.parent_block.broadcast_address == str(self.network):
                        # todo: better error message
                        raise ValidationError('broadcast address')

        if self.prefixlen < self.network.max_prefixlen:
            if not self.use_reserved_addresses:
                try:
                    if self.network_address == str(
                        self.child_blocks.first()
                    ):
                        # todo: better error message
                        raise ValidationError('network address')
                except IndexError:
                    pass

                if self.family == 4:
                    try:
                        if self.broadcast_address == str(
                                self.child_blocks.order_by('-network').first()
                        ):
                            # todo: better error message
                            raise ValidationError('broadcast address')
                    except IndexError:
                        pass

        return cleaned_data

    @classmethod
    def from_db(cls, db, field_names, values):
        """
        todo: figure out why this is overridden...
        """
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance
