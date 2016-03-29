"""
configs resources app configuration.
"""
from django.apps import AppConfig
from cidrfield.fields import CidrField
from cidrfield.lookups import NetContains, NetContained


class ResourcesConfig(AppConfig):
    """
    configuration for the resource app.
    """

    name = 'resources'
    verbose_name = 'Resource Management'

    def ready(self):
        CidrField.register_lookup(NetContains)
        CidrField.register_lookup(NetContained)
