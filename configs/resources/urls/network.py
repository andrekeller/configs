"""
confi.gs network urls.
"""
# django
from django.conf.urls import url
# confi.gs
from ..views import NetworkCreate
from ..views import NetworkDelete
from ..views import NetworkDetail
from ..views import NetworkList
from ..views import NetworkUpdate

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
