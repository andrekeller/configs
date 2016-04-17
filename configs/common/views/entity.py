"""
confi.gs common app entity views.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from common.models import Entity


class EntityMixin(LoginRequiredMixin):
    """
    mixin for common entity view settings
    """
    model = Entity
    success_url = reverse_lazy('resources:entity-list')


class EntityModifyMixin(EntityMixin):
    """
    mixin for common data-modifying entity view settings
    """
    fields = [
        'name',
    ]


class EntityList(EntityMixin, ListView):
    """
    view to list all entities
    """


class EntityCreate(EntityModifyMixin, CreateView):
    """
    view to create a new entity
    """


class EntityUpdate(EntityModifyMixin, UpdateView):
    """
    view to edit an existing entity
    """


class EntityDelete(EntityMixin, DeleteView):
    """
    view to delete an entity
    """
