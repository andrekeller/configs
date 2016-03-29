"""
configs common models.
"""
from django.db import models
from .fields import TagField


class Tag(models.Model):
    name = TagField(max_length=64, unique=True)

    def __str__(self):
        return "%s" % self.name
