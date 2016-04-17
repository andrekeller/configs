"""
confi.gs vlan urls.
"""
# django
from django.conf.urls import url
# confi.gs
from ..views import VlanCreate
from ..views import VlanDelete
from ..views import VlanUpdate

urlpatterns = [
    url(r'^new$', VlanCreate.as_view(), name='vlan-new'),
    url(r'^new/(?P<parent>\d+)$', VlanCreate.as_view(), name='vlan-new'),
    url(r'^edit/(?P<pk>\d+)$', VlanUpdate.as_view(), name='vlan-edit'),
    url(r'^delete/(?P<pk>\d+)$', VlanDelete.as_view(), name='vlan-delete'),
]
