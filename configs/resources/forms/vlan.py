"""
confi.gs vlan forms
"""
from .mixins import ParentModelForm
from ..models import Vlan, Vrf


class VlanForm(ParentModelForm):
    """
    confi.gs vlan form
    """
    parent_model = Vrf

    class Meta:
        model = Vlan
        fields = [
            'vlan_id',
            'vlan_name',
            'vrf',
        ]
