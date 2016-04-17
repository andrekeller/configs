"""
confi.gs domain urls
"""
# django
from django.conf.urls import url
# confi.gs
from ..views import DomainCreate
from ..views import DomainDelete
from ..views import DomainDetail
from ..views import DomainList
from ..views import DomainUpdate

urlpatterns = [
    url(r'^$', DomainList.as_view(), name='domain-list'),
    url(r'^(?P<pk>\d+)$', DomainDetail.as_view(), name='domain-detail'),
    url(r'^new$', DomainCreate.as_view(), name='domain-new'),
    url(r'^edit/(?P<pk>\d+)$', DomainUpdate.as_view(), name='domain-edit'),
    url(r'^delete/(?P<pk>\d+)$', DomainDelete.as_view(), name='domain-delete'),
]
