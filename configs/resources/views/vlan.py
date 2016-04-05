"""
configs resources app vlan views.
"""
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from resources.forms import VlanForm
from resources.models import Vlan, Vrf
from .mixins import ParentCreateMixin, ParentModifyMixin


class VlanMixin(LoginRequiredMixin):
    model = Vlan
    parent_model = Vrf
    success_url = reverse_lazy('resources:vrf-list')


class VlanModifyMixin(VlanMixin, ParentModifyMixin):
    form_class = VlanForm

    def get_success_url(self):
        try:
            return reverse_lazy('resources:vrf-detail',
                                kwargs={'pk': self.object.vrf.id})
        except AttributeError:
            return reverse_lazy('resources:vrf-list')


class VlanCreate(VlanModifyMixin, ParentCreateMixin, CreateView):
    pass


class VlanUpdate(VlanModifyMixin, UpdateView):
    pass


class VlanDelete(VlanModifyMixin, DeleteView):
    pass
