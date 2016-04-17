"""
confi.gs resources vlan models
"""
# django
from django.core.exceptions import ValidationError
from django.db import models
# confi.gs
from common.models.mixins import ValidateModelMixin
from .network import Network


class Vlan(ValidateModelMixin, models.Model):
    """
    confi.gs vlan model
    """
    vlan_id = models.IntegerField()
    vlan_name = models.CharField(max_length=255)
    vrf = models.ForeignKey('resources.Vrf',
                            default=1,
                            on_delete=models.SET_DEFAULT)

    class Meta:
        ordering = ['vlan_id']
        unique_together = ("vlan_id", "vrf")

    def __str__(self):
        """
        returns string representation of vlan object
        """
        return "VLAN%04d: %s (%s)" % (self.vlan_id, self.vlan_name, self.vrf)

    @property
    def networks(self):
        """
        returns networks assigned to this vlan as a QuerySet
        """
        return Network.objects.filter(vlan=self.pk)

    def clean(self):
        """
        prevent changing vrf of vlan with assigned networks
        """
        if self.pk is not None:
            if self.networks:
                orig = Vlan.objects.get(pk=self.pk)
                if not orig.vrf == self.pk:
                    raise ValidationError(
                        "VRF change on vlan with networks prohibited"
                    )
