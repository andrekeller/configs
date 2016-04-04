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
    model = Vrf
    success_url = reverse_lazy('resources:vrf-list')


class VrfModifyMixin(VrfMixin):
    fields = [
        'name',
    ]


class VrfCreate(VrfModifyMixin, CreateView):
    pass


class VrfDelete(VrfMixin, DeleteView):

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except IntegrityError as exc:
            return render(request,
                          'resources/vrf_delete_failed.html',
                          {'vrf_pk': kwargs['pk']})


class VrfDetail(VrfMixin, DetailView):
    pass


class VrfList(VrfMixin, ListView):
    pass


class VrfUpdate(VrfModifyMixin, UpdateView):
    pass

