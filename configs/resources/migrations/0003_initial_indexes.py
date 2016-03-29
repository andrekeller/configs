from django.db import migrations
from cidrfield.migrations.operations import AddCidrIndex


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0002_initial_functions'),
    ]

    operations = [
        AddCidrIndex(
            table='resources_network',
            field='network',
        ),
    ]
