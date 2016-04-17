"""
confi.gs vrf api resources
"""
# 3rd-party
from tastypie.resources import ModelResource
# confi.gs
from api.mixins import AuthMixin
from resources.models import Vrf


class VrfResource(ModelResource):
    """
    confi.gs vrf api resource
    """

    class Meta(AuthMixin):
        queryset = Vrf.objects.all()
        resource_name = 'vrf'
        limit = 0
        max_limit = None
