"""
confi.gs networkgroup views
"""
# django
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
# confi.gs
from resources.models import NetworkGroup


class NetworkGroupMixin(LoginRequiredMixin):
    """
    mixin for common networkgroup view settings
    """
    model = NetworkGroup
    success_url = reverse_lazy('resources:network-list')


class NetworkGroupModifyMixin(NetworkGroupMixin):
    """
    mixin for common data-modifying networkgroup view settings
    """
    fields = [
        'name',
    ]


class NetworkGroupCreate(NetworkGroupModifyMixin, CreateView):
    """
    view to create a new networkgroup
    """


class NetworkGroupDelete(NetworkGroupMixin, DeleteView):
    """
    view to delete a networkgroup
    """


class NetworkGroupUpdate(NetworkGroupModifyMixin, UpdateView):
    """
    view to edit an existing networkgroup
    """
