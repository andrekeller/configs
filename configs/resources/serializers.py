"""
configs resources app REST-API serializers.
"""
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Network, Vlan, Vrf


class ParentNetworkSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for parent network
    """
    links = serializers.SerializerMethodField()

    class Meta:
        model = Network
        fields = (
            'id',
            'network',
            'links',
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('network-detail',
                            kwargs={'pk': obj.pk}, request=request),
        }


class ChildrenNetworkSerializer(serializers.HyperlinkedModelSerializer):
    """
    child network serializer
    """
    links = serializers.SerializerMethodField()

    class Meta:
        model = Network
        fields = (
            'id',
            'network',
            'links',
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('network-detail',
                            kwargs={'pk': obj.pk}, request=request),
        }


class VrfSerializer(serializers.HyperlinkedModelSerializer):
    """
    vrf serializer
    """
    links = serializers.SerializerMethodField()

    class Meta:
        model = Vrf
        fields = (
            'name',
            'links',
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse(
                'vrf-detail',
                kwargs={'pk': obj.pk},
                request=request,
            ),
        }


class VlanSerializer(serializers.HyperlinkedModelSerializer):
    """
    vlan serializer
    """
    links = serializers.SerializerMethodField()
    vrf_details = VrfSerializer(read_only=True, source='vrf')

    class Meta:
        model = Vlan
        fields = (
            'id',
            'vlan_id',
            'vlan_name',
            'vrf',
            'vrf_details',
            'links',
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse(
                'vlan-detail',
                kwargs={'pk': obj.pk},
                request=request,
            ),
        }


class NetworkSerializer(serializers.HyperlinkedModelSerializer):
    """
    network serializer
    """
    child_blocks = ChildrenNetworkSerializer(many=True, read_only=True)
    parent_block = ParentNetworkSerializer(read_only=True)
    vrf_details = VrfSerializer(read_only=True, source='vrf')
    vlan_details = VlanSerializer(read_only=True, source='vlan')
    links = serializers.SerializerMethodField()

    class Meta:
        model = Network
        fields = ('id',
                  'network',
                  'vrf',
                  'vrf_details',
                  'vlan',
                  'vlan_details',
                  'use_reserved_addresses',
                  'network_address',
                  'prefixlen',
                  'broadcast_address',
                  'family',
                  'num_addresses',
                  'assigned',
                  'allocated',
                  'parent_block',
                  'child_blocks',
                  'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse(
                'network-detail',
                kwargs={'pk': obj.pk},
                request=request,
            ),
        }

    def validate(self, attrs):
        instance = Network(**attrs)
        instance.clean()
        return attrs

