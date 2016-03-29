"""
configs resources app network view urls.
"""
from django.conf.urls import url
from ..views import NetworkCreate, NetworkDelete, NetworkDetail, NetworkList, \
    NetworkUpdate

urlpatterns = [
    url(r'^$',
        NetworkList.as_view(), name='network-list'),
    url(r'^(?P<pk>\d+)$',
        NetworkDetail.as_view(), name='network-detail'),
    url(r'^new$',
        NetworkCreate.as_view(), name='network-new'),
    url(r'^new/(?P<parent>\d+)$',
        NetworkCreate.as_view(), name='network-new'),
    url(r'^new/(?P<parent>\d+)/(?P<prefixlen>\d+)$',
        NetworkCreate.as_view(), name='network-new'),
    url(r'^edit/(?P<pk>\d+)$',
        NetworkUpdate.as_view(), name='network-edit'),
    url(r'^delete/(?P<pk>\d+)$',
        NetworkDelete.as_view(), name='network-delete'),
]
