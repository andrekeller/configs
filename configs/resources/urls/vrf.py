"""
confi.gs resources app vrf urls
"""

from django.conf.urls import url
from ..views import VrfCreate, VrfDelete, VrfDetail, VrfList, VrfUpdate

urlpatterns = [
    url(r'^$', VrfList.as_view(), name='vrf-list'),
    url(r'^(?P<pk>\d+)$', VrfDetail.as_view(), name='vrf-detail'),
    url(r'^new$', VrfCreate.as_view(), name='vrf-new'),
    url(r'^edit/(?P<pk>\d+)$', VrfUpdate.as_view(), name='vrf-edit'),
    url(r'^delete/(?P<pk>\d+)$', VrfDelete.as_view(), name='vrf-delete'),
]
