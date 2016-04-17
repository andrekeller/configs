"""
confi.gs network views.
"""
# django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
# confi.gs
from resources.models import Network
from resources.models import Vlan
from ..forms import NetworkForm


class NetworkMixin(LoginRequiredMixin):
    """
    mixin for common network view settings
    """
    model = Network


class NetworkModifyMixin(NetworkMixin, ContextMixin):
    #todo: parentmodifymixin?
    """
    mixin for common data-modifying network view settings
    """
    form_class = NetworkForm

    def get_context_data(self, **kwargs):
        """
        add possible vlans to context data.
        """
        context = super().get_context_data(**kwargs)
        try:
            if context['network'].vrf.id:
                context['vlans'] = Vlan.objects.filter(
                    vrf__id=context['network'].vrf.id
                )
        except (AttributeError, KeyError):
            context['vlans'] = Vlan.objects.filter(vrf__id=1)

        return context


class NetworkCreate(NetworkModifyMixin, CreateView):
    #todo: parentcreatemixin?
    """
    view to create a new network
    """

    def get_success_url(self):
        """
        returns a success url to redirect after modify operation
        """
        try:
            return reverse_lazy('resources:network-detail',
                                kwargs={'pk': self.object.parent_block.id})
        except AttributeError:
            return reverse_lazy('resources:network-list')

    def get_context_data(self, **kwargs):
        """
        We add additional context variables if called with parent argument.
        This is needed so we can generate appropriate breadcrumb links in the
        create form.
        """
        context = super().get_context_data(**kwargs)

        try:
            context['network'] = Network.objects.get(
                pk=context['view'].kwargs['parent']
            )
            context['create'] = True
        except (KeyError, ObjectDoesNotExist):
            pass

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs


class NetworkDetail(NetworkMixin, DetailView):
    """
    view for network details
    """


class NetworkDelete(NetworkMixin, DeleteView):
    #todo: parentmodifymixin?
    """
    view to delete a network
    """

    def get_success_url(self):
        """
        returns a success url to redirect after modify operation
        """
        try:
            return reverse_lazy('resources:network-detail',
                                kwargs={'pk': self.object.parent_block.id})
        except AttributeError:
            return reverse_lazy('resources:network-list')


class NetworkList(NetworkMixin, ListView):
    """
    view to list all networks
    """
    queryset = Network.root_objects.all().select_related('vlan', 'vrf')


class NetworkUpdate(NetworkModifyMixin, UpdateView):
    #todo: parentmodifymixin?
    """
    view to edit an existing network
    """
