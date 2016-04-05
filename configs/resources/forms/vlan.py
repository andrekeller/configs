from ..models import Vlan, Vrf
from .mixins import ParentModelForm


class VlanForm(ParentModelForm):
    parent_model = Vrf

    class Meta:
        model = Vlan
        fields = [
            'vlan_id',
            'vlan_name',
            'vrf',
        ]
