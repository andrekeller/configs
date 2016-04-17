"""
confi.gs resources urls
"""
from django.conf.urls import include
from django.conf.urls import url
from . import domain
from . import host
from . import network
from . import vlan
from . import vrf

urlpatterns = [
    url(r'^domain/', include(domain)),
    url(r'^host/', include(host)),
    url(r'^network/', include(network)),
    url(r'^vlan/', include(vlan)),
    url(r'^vrf/', include(vrf)),
]
