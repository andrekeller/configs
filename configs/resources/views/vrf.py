"""
confi.gs resources app vrf views.
"""
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from resources.models import Vrf


class VrfMixin(LoginRequiredMixin):
    """
    mixin for common vrf view settings
    """
    model = Vrf
    success_url = reverse_lazy('resources:vrf-list')


class VrfModifyMixin(VrfMixin):
    """
    mixin for common data-modifying vrf view settings
    """
    fields = [
        'name',
    ]


class VrfCreate(VrfModifyMixin, CreateView):
    """
    view to create a vrf
    """


class VrfDelete(VrfMixin, DeleteView):
    """
    view to delete a vrf
    """

    def delete(self, request, *args, **kwargs):
        """
        override delete to display a error message, when deleting a vrf
        would cause conflicting vlans/networks in the default vrf.
        """
        try:
            return super().delete(request, *args, **kwargs)
        except IntegrityError as exc:
            return render(request,
                          'resources/vrf_delete_failed.html',
                          {'vrf_pk': kwargs['pk']})


class VrfDetail(VrfMixin, DetailView):
    """
    view for vrf details
    """


class VrfList(VrfMixin, ListView):
    """
    view to list all vrfs
    """


class VrfUpdate(VrfModifyMixin, UpdateView):
    """
    views to edit an existing vrf
    """
