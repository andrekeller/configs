"""
configs resources app network views.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from resources.models import Network, Vlan
from ..forms import NetworkForm


class NetworkMixin(LoginRequiredMixin):
    model = Network


class NetworkModifyMixin(NetworkMixin, ContextMixin):
    form_class = NetworkForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if context['network'].vrf.id:
                context['vlans'] = Vlan.objects.filter(
                    vrf__id=context['network'].vrf.id
                )
        except (AttributeError, KeyError):
            context['vlans'] = Vlan.objects.filter(vrf__id=1)

        return context


class NetworkList(NetworkMixin, ListView):
    queryset = Network.get_root_blocks()


class NetworkDetail(NetworkMixin, DetailView):
    pass


class NetworkCreate(NetworkModifyMixin, CreateView):

    def get_success_url(self):
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


class NetworkUpdate(NetworkModifyMixin, UpdateView):
    pass


class NetworkDelete(NetworkMixin, DeleteView):
    def get_success_url(self):
        try:
            return reverse_lazy('resources:network-detail',
                                kwargs={'pk': self.object.parent_block.id})
        except AttributeError:
            return reverse_lazy('resources:network-list')
