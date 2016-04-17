"""
confi.gs network api resources
"""
# 3rd-party
from tastypie import fields
from tastypie.resources import ALL
from tastypie.resources import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
# confi.gs
from api.validation import FormValidation
from api.mixins import AuthMixin
from resources.forms import NetworkForm
from resources.models import Network


class NetworkResource(ModelResource):
    """
    confi.gs network api resource
    """
    vlan = fields.ForeignKey('resources.api.vlan.VlanResource', 'vlan' ,null=True, blank=True)
    vrf = fields.ForeignKey('resources.api.vrf.VrfResource', 'vrf')

    class Meta(AuthMixin):
        queryset = Network.objects.all().select_related('vlan', 'vrf')
        limit = 100
        max_limit = None
        resource_name = 'network'
        filtering = {
            'network': ALL,
            'vlan': ALL_WITH_RELATIONS,
            'vrf': ALL_WITH_RELATIONS,
        }
        validation = FormValidation(form_class=NetworkForm)
