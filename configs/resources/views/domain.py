"""
configs resources app domain views.
"""
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from resources.models import Domain


class DomainMixin(LoginRequiredMixin):
    model = Domain
    success_url = reverse_lazy('resources:domain-list')


class DomainModifyMixin(DomainMixin):
    fields = [
        'name',
    ]


class DomainDetail(DomainMixin, DetailView):
    pass


class DomainList(DomainMixin, ListView):
    pass


class DomainCreate(DomainModifyMixin, CreateView):
    pass


class DomainUpdate(DomainModifyMixin, UpdateView):
    pass


class DomainDelete(DomainMixin, DeleteView):
    pass
