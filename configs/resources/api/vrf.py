from tastypie.resources import ModelResource
from resources.models import Vrf


class VrfResource(ModelResource):

    class Meta:
        queryset = Vrf.objects.all()
        resource_name = 'vrf'
        limit = 0
        max_limit = None
