from django import forms
from django.core.exceptions import ObjectDoesNotExist
from ..models import Network


class NetworkForm(forms.ModelForm):

    def __init__(self, parent=None, prefixlen=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None
        self.prefixlen = None
        try:
            self.parent = Network.objects.get(id=parent)
            if self.parent.is_host:
                if self.parent.parent_block:
                    self.parent = parent.parent_block
        except ObjectDoesNotExist:
            pass

        if self.parent:
            if prefixlen is None:
                prefixlen = self.parent.max_prefixlen
            self.next = self.parent.next
            self.fields['network'].initial = self.next(prefixlen)

    class Meta:
        model = Network
        fields = [
            'network',
            'use_reserved_addresses',
            'description',
            'vrf',
            'vlan',
            'status',
            'host',
            'tags',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, }),
        }


