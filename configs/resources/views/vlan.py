"""
confi.gs vlan views.
"""
# django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
# confi.gs
from common.views.mixins import ParentCreateMixin
from common.views.mixins import ParentModifyMixin
from resources.forms import VlanForm
from resources.models import Vlan
from resources.models import Vrf


class VlanMixin(LoginRequiredMixin):
    """
    mixin for common vlan view settings
    """
    model = Vlan
    parent_model = Vrf
    success_url = reverse_lazy('resources:vrf-list')


class VlanModifyMixin(VlanMixin, ParentModifyMixin):
    """
    mixin for common data-modifying vlan view settings
    """
    form_class = VlanForm

    def get_success_url(self):
        """
        returns a success url to redirect after modify operation
        """
        try:
            return reverse_lazy('resources:vrf-detail',
                                kwargs={'pk': self.object.vrf.id})
        except AttributeError:
            return reverse_lazy('resources:vrf-list')


class VlanCreate(VlanModifyMixin, ParentCreateMixin, CreateView):
    """
    view to create a new vlan
    """


class VlanDelete(VlanModifyMixin, DeleteView):
    """
    view to delete a vlan
    """


class VlanUpdate(VlanModifyMixin, UpdateView):
    """
    view to update an existing vlan
    """
