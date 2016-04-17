"""
confi.gs domain views
"""
# django
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
# confi.gs
from resources.models import Domain


class DomainMixin(LoginRequiredMixin):
    """
    mixin for common domain view settings
    """
    model = Domain
    success_url = reverse_lazy('resources:domain-list')


class DomainModifyMixin(DomainMixin):
    """
    mixin for common data-modifying domain view settings
    """
    fields = [
        'name',
    ]


class DomainCreate(DomainModifyMixin, CreateView):
    """
    view to create a new domain
    """


class DomainDelete(DomainMixin, DeleteView):
    """
    view to delete a domain
    """


class DomainDetail(DomainMixin, DetailView):
    """
    view for domain details
    """


class DomainList(DomainMixin, ListView):
    """
    view to list all domains
    """


class DomainUpdate(DomainModifyMixin, UpdateView):
    """
    view to edit an existing domain
    """
