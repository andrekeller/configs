from django.db import models
from django.core.exceptions import ValidationError
from .mixins import ValidateModelMixin
from .network import Network


class Vlan(ValidateModelMixin, models.Model):
    """
    model to represent VLANs
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
        return "VLAN%04d: %s (%s)" % (self.vlan_id, self.vlan_name, self.vrf)

    @property
    def networks(self):
        return Network.objects.filter(vlan=self.pk)

    def clean(self):
        if self.pk is not None:
            if self.networks:
                orig = Vlan.objects.get(pk=self.pk)
                if not orig.vrf == self.pk:
                    raise ValidationError(
                        "VRF change on vlan with networks prohibited"
                    )
