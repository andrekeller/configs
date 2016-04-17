"""
confi.gs resources app configuration.
"""
# django
from django.apps import AppConfig
# confi.gs
from cidrfield.fields import CidrField
from cidrfield.lookups import NetContains
from cidrfield.lookups import NetContained


class ResourcesConfig(AppConfig):
    """
    configuration for the confi.gs resource app.
    """

    name = 'resources'
    verbose_name = 'Resource Management'

    def ready(self):
        """
        register cidrfield lookups..
        """
        CidrField.register_lookup(NetContains)
        CidrField.register_lookup(NetContained)
