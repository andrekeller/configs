"""
confi.gs resources vrf models
"""
# django
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
# confi.gs
from common.models.mixins import ValidateModelMixin


class Vrf(ValidateModelMixin, models.Model):
    """
    confi.gs vrf model
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """
        returns string representation of vrf object
        """
        if self.pk == 1 and not self.name == 'default':
            return "%s [DEFAULT]" % self.name
        return "%s" % self.name

    @property
    def default(self):
        """
        returns wheter or not this vrf is the default vrf
        """
        if self.pk == 1:
            return True
        return False

    def get_absolute_url(self):
        """
        returns a canonical url for vrf object
        """
        return reverse('resources:vrf-detail', args=[self.pk])


@receiver(pre_delete, sender=Vrf)
def protect_default_vlan(sender, instance, **kwargs):
    """
    signal receiver to prevent that the default vlan can be deleted.
    """
    if instance.default:
        raise PermissionDenied("default vrf may not be deleted.")
