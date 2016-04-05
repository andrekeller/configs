"""
configs resources app domain views.
"""
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from resources.forms import HostForm
from resources.models import Host, Domain
from .mixins import ParentCreateMixin, ParentModifyMixin


class HostMixin(LoginRequiredMixin):
    model = Host
    parent_model = Domain
    success_url = reverse_lazy('resources:domain-list')


class HostModifyMixin(HostMixin, ParentModifyMixin):
    form_class = HostForm

    def get_success_url(self):
        try:
            return reverse_lazy('resources:domain-detail',
                                kwargs={'pk': self.object.domain.id})
        except AttributeError:
            return reverse_lazy('resources:domain-list')


class HostDetail(HostMixin, DetailView):
    pass


class HostCreate(HostModifyMixin, ParentCreateMixin, CreateView):
    pass


class HostUpdate(HostModifyMixin, UpdateView):
    pass


class HostDelete(HostModifyMixin, DeleteView):
    pass
