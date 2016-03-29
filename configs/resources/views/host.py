"""
configs resources app domain views.
"""
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from resources.forms import HostForm
from resources.models import Host, Domain


class HostMixin(LoginRequiredMixin):
    model = Host
    success_url = reverse_lazy('resources:domain-list')


class HostModifyMixin(HostMixin, ContextMixin):
    form_class = HostForm

    def get_success_url(self):
        try:
            return reverse_lazy('resources:domain-detail',
                                kwargs={'pk': self.object.domain.id})
        except AttributeError:
            return reverse_lazy('resources:domain-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['domain'] = Domain.objects.filter(
                host=context['view'].kwargs['pk']
            ).first()
        except (KeyError, ObjectDoesNotExist):
            pass

        return context


class HostDetail(HostMixin, DetailView):
    pass


class HostCreate(HostModifyMixin, CreateView):
    def get_context_data(self, **kwargs):
        """
        We add additional context variables if called with domain argument.
        This is needed so we can generate appropriate breadcrumb links in the
        create form.
        """
        context = super().get_context_data(**kwargs)

        try:
            context['domain'] = Domain.objects.get(
                pk=context['view'].kwargs['domain'])
            context['create'] = True
        except (KeyError, ObjectDoesNotExist):
            pass

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs


class HostUpdate(HostModifyMixin, UpdateView):
    pass


class HostDelete(HostMixin, DeleteView):
    pass
