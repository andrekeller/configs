"""
confi.gs common tag models
"""
# django
from django.db import models
# confi.gs
from common.fields import TagField


class Tag(models.Model):
    """
    model to represent tags used across the confi.gs apps.
    """
    name = TagField(max_length=64, unique=True)

    def __str__(self):
        return "%s" % self.name
