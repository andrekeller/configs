"""
configs resources app vlan view urls.
"""
from django.conf.urls import url
from ..views import DomainCreate, DomainDelete, DomainDetail, DomainList,\
    DomainUpdate

urlpatterns = [
    url(r'^$', DomainList.as_view(), name='domain-list'),
    url(r'^(?P<pk>\d+)$', DomainDetail.as_view(), name='domain-detail'),
    url(r'^new$', DomainCreate.as_view(), name='domain-new'),
    url(r'^edit/(?P<pk>\d+)$', DomainUpdate.as_view(),
        name='domain-edit'),
    url(r'^delete/(?P<pk>\d+)$', DomainDelete.as_view(),
        name='domain-delete'),
]
