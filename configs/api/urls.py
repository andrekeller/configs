from django.conf.urls import url, include

from tastypie.api import Api

from resources.api import NetworkResource
from resources.api import VlanResource
from resources.api import VrfResource

v1_api = Api(api_name='v1')
v1_api.register(NetworkResource())
v1_api.register(VlanResource())
v1_api.register(VrfResource())

urlpatterns = [
    url(r'', include(v1_api.urls)),
]
