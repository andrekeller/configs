from django.db import models

"""
models related to entity (customers, partners, etc.) management
"""


class Entity(models.Model):
    """
    model to represent entities (customers, partners, etc.)
    """
    name = models.CharField(unique=True, max_length=255)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """
        string representation of entity object
        :rtype: str
        """
        return "%s" % self.name
