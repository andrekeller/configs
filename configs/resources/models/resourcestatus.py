from django.db import models
from .mixins import ValidateModelMixin


class ResourceStatus(ValidateModelMixin, models.Model):
    """
    model to represent the different resource statuses.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "%s" % self.name
