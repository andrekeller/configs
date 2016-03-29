from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.exceptions import PermissionDenied
from .mixins import ValidateModelMixin


class Vrf(ValidateModelMixin, models.Model):
    """
    model to represent VRFs
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        if self.pk == 1 and not self.name == 'default':
            return "%s [DEFAULT]" % self.name
        return "%s" % self.name

    @property
    def default(self):
        if self.pk == 1:
            return True
        return False


@receiver(pre_delete, sender=Vrf)
def protect_default_vlan(sender, instance, **kwargs):
    if instance.default:
        raise PermissionDenied("default vrf may not be deleted.")
