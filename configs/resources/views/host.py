"""
confi.gs host views.
"""
# django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
# confi.gs
from common.views.mixins import ParentCreateMixin
from common.views.mixins import ParentModifyMixin
from resources.forms import HostForm
from resources.models import Host, Domain


class HostMixin(LoginRequiredMixin):
    """
    mixin for common host view settings
    """
    model = Host
    parent_model = Domain
    success_url = reverse_lazy('resources:domain-list')


class HostModifyMixin(HostMixin, ParentModifyMixin):
    """
    mixin for common data-modifying host view settings
    """
    form_class = HostForm

    def get_success_url(self):
        """
        returns a success url to redirect after modify operation
        """
        try:
            return reverse_lazy('resources:domain-detail',
                                kwargs={'pk': self.object.domain.id})
        except AttributeError:
            return reverse_lazy('resources:domain-list')


class HostCreate(HostModifyMixin, ParentCreateMixin, CreateView):
    """
    view to create a new host
    """


class HostDelete(HostModifyMixin, DeleteView):
    """
    view to delete a host
    """


class HostDetail(HostMixin, DetailView):
    """
    view for host details
    """


class HostUpdate(HostModifyMixin, UpdateView):
    """
    view to update an existing host
    """
