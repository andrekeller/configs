"""
configs resources app urls.
"""
from django.conf.urls import include, url
from . import domain, host, network, vlan

urlpatterns = [
    url(r'^domain/', include(domain)),
    url(r'^host/', include(host)),
    url(r'^network/', include(network)),
    url(r'^vlan/', include(vlan)),
]
