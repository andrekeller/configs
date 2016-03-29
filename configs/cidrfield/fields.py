"""
configs cidr field.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .forms.fields import CidrField as CidrFormField
from . import IPv4Network, IPv6Network
from .validators import validate_network


class CidrField(models.Field):
    """
    CidrField model field.
    """

    description = _("An IPv4 or IPv6 address represented in CIDR notation")
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 43
        super(CidrField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CidrField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def db_type(self, connection):
        return 'cidr'

    def formfield(self, **kwargs):
        defaults = {'form_class': CidrFormField}
        defaults.update(kwargs)
        return super(CidrField, self).formfield(**defaults)

    def get_prep_lookup(self, lookup_type, value):
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        if not value:
            return None
        if isinstance(value, (IPv4Network, IPv6Network)):
            return value.exploded

        return value

    def to_python(self, value):
        return validate_network(value)

    def from_db_value(self, value, expression, connection, context):
        return validate_network(value)


