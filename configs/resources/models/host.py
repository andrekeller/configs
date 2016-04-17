"""
confi.gs resources host models
"""
# django
from django.contrib.postgres.fields import HStoreField
from django.core.urlresolvers import reverse
from django.db import models
# 3rd-party
from tagging.fields import TagField


class Host(models.Model):
    """
    confi.gs host model
    """
    name = models.CharField(max_length=255)
    domain = models.ForeignKey('resources.Domain')
    encdata = HStoreField(blank=True, null=True)
    tags = TagField()

    class Meta:
        unique_together = ("name", "domain")

    def __str__(self):
        """
        string representation of host object
        """
        return "%s.%s" % (self.name, self.domain.name)

    def get_absolute_url(self):
        """
        canonical url for a host object
        """
        return reverse('resources:host-detail', args=[self.pk])


class Domain(models.Model):
    """
    confi.gs domain model
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        string representation of domain object
        """
        return "%s" % self.name

    def get_absolute_url(self):
        """
        canonical url for a domain object
        """
        return reverse('resources:domain-detail', args=[self.pk])

