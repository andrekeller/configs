"""
configs resources app vlan view urls.
"""
from django.conf.urls import url
from ..views import VlanCreate, VlanDelete, VlanList, VlanUpdate

urlpatterns = [
    url(r'^$', VlanList.as_view(), name='vlan-list'),
    url(r'^new$', VlanCreate.as_view(), name='vlan-new'),
    url(r'^edit/(?P<pk>\d+)$', VlanUpdate.as_view(),
        name='vlan-edit'),
    url(r'^delete/(?P<pk>\d+)$', VlanDelete.as_view(),
        name='vlan-delete'),
]
