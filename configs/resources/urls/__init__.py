"""
confi.gs resources urls
"""
# django
from django.conf.urls import include
from django.conf.urls import url
# confi.gs
from resources.urls import domain
from resources.urls import host
from resources.urls import network
from resources.urls import networkgroup
from resources.urls import vlan
from resources.urls import vrf

urlpatterns = [
    url(r'^domain/', include(domain)),
    url(r'^host/', include(host)),
    url(r'^network/', include(network)),
    url(r'^networkgroup/', include(networkgroup)),
    url(r'^vlan/', include(vlan)),
    url(r'^vrf/', include(vrf)),
]
