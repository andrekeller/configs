"""
configs resources app views.
"""
# TODO: make imports explicit
from .domain import *
# TODO: make imports explicit
from .host import *
from .network import NetworkCreate, NetworkDelete, NetworkDetail, \
    NetworkList, NetworkUpdate
from .vlan import VlanCreate, VlanDelete, VlanUpdate
from .vrf import VrfCreate, VrfDelete, VrfDetail, VrfList, VrfUpdate
