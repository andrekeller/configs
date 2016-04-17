"""
confi.gs vlan api resources
"""
# 3rd-party
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
# confi.gs
from api.mixins import AuthMixin
from resources.models import Vlan


class VlanResource(ModelResource):
    """
    confi.gs vlan api resource
    """
    vrf = fields.ForeignKey('resources.api.vrf.VrfResource', 'vrf')

    class Meta(AuthMixin):
        queryset = Vlan.objects.all()
        limit = 0
        max_limit = None
        resource_name = 'vlan'
        filtering = {
            'vlan_id': ALL,
            'vrf': ALL_WITH_RELATIONS,
        }
