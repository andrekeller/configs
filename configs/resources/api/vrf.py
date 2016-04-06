from tastypie.resources import ModelResource
from api.mixins import AuthMixin
from resources.models import Vrf


class VrfResource(ModelResource):

    class Meta(AuthMixin):
        queryset = Vrf.objects.all()
        resource_name = 'vrf'
        limit = 0
        max_limit = None
