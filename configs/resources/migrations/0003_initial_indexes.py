"""
confi.gs resources additional index migrations
"""
from django.db import migrations
from cidrfield.migrations.operations import AddCidrIndex


class Migration(migrations.Migration):
    """
    confi.gs resources initial additional index migration
    """
    dependencies = [
        ('resources', '0002_initial_functions'),
    ]

    operations = [
        AddCidrIndex(
            table='resources_network',
            field='network',
        ),
    ]
