from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from resources.models import Vlan


class VlanResource(ModelResource):
    vrf = fields.ForeignKey('resources.api.vrf.VrfResource', 'vrf')

    class Meta:
        queryset = Vlan.objects.all()
        limit = 0
        max_limit = None
        resource_name = 'vlan'
        filtering = {
            'vlan_id': ALL,
            'vrf': ALL_WITH_RELATIONS,
        }
