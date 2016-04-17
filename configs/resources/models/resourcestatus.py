"""
confi.gs resources status models
"""
# django
from django.db import models
# confi.gs
from common.models.mixins import ValidateModelMixin


class ResourceStatus(ValidateModelMixin, models.Model):
    """
    model representing different resource statuses.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        returns a string representation of resource status object
        """
        return "%s" % self.name
