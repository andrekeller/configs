"""
configs cidr form field.

django formfield to represent cidr field in django forms.
"""
from django.forms.fields import CharField


class CidrField(CharField):
    """
    cidr form field.
    """
    pass
