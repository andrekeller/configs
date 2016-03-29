"""
configs resources app vlan views.
"""
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from resources.models import Vlan


class VlanMixin(LoginRequiredMixin):
    model = Vlan
    success_url = reverse_lazy('resources:vlan-list')


class VlanModifyMixin(VlanMixin):
    fields = [
        'vlan_id',
        'vlan_name',
        'vrf',
    ]


class VlanList(VlanMixin, ListView):
    pass


class VlanCreate(VlanModifyMixin, CreateView):
    pass


class VlanUpdate(VlanModifyMixin, UpdateView):
    pass


class VlanDelete(VlanMixin, DeleteView):
    pass
