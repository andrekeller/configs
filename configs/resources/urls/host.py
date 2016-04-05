"""
configs resources app vlan view urls.
"""
from django.conf.urls import url
from ..views import HostCreate, HostDelete, HostDetail, HostUpdate

urlpatterns = [
    url(r'^(?P<pk>\d+)$', HostDetail.as_view(), name='host-detail'),
    url(r'^new$', HostCreate.as_view(), name='host-new'),
    url(r'^new/(?P<parent>\d+)$', HostCreate.as_view(), name='host-new'),
    url(r'^edit/(?P<pk>\d+)$', HostUpdate.as_view(), name='host-edit'),
    url(r'^delete/(?P<pk>\d+)$', HostDelete.as_view(), name='host-delete'),
]
