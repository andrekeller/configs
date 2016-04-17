"""
confi.gs host urls
"""
# django
from django.conf.urls import url
# confi.gs
from ..views import HostCreate
from ..views import HostDelete
from ..views import HostDetail
from ..views import HostUpdate

urlpatterns = [
    url(r'^(?P<pk>\d+)$', HostDetail.as_view(), name='host-detail'),
    url(r'^new$', HostCreate.as_view(), name='host-new'),
    url(r'^new/(?P<parent>\d+)$', HostCreate.as_view(), name='host-new'),
    url(r'^edit/(?P<pk>\d+)$', HostUpdate.as_view(), name='host-edit'),
    url(r'^delete/(?P<pk>\d+)$', HostDelete.as_view(), name='host-delete'),
]
