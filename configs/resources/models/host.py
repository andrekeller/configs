from django.contrib.postgres.fields import HStoreField
from django.core.urlresolvers import reverse
from django.db import models
from tagging.fields import TagField


class Host(models.Model):
    name = models.CharField(max_length=255)
    domain = models.ForeignKey('resources.Domain')
    encdata = HStoreField(blank=True, null=True)
    tags = TagField()

    class Meta:
        unique_together = ("name", "domain")

    def __str__(self):
        return "%s.%s" % (self.name, self.domain.name)

    def get_absolute_url(self):
        """
        canonical url for domain object

        :returns: url
        :rtype: str
        """
        return reverse('resources:host-detail', args=[self.pk])


class Domain(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        """
        canonical url for domain object

        :returns: url
        :rtype: str
        """
        return reverse('resources:domain-detail', args=[self.pk])

