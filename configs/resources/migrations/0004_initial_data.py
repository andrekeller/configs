"""
confi.gs resources initial data migrations
"""
from django.db import migrations
from django.core.management import call_command

fixture = 'configs_defaults'


def load_fixture(apps, schema_editor):
    """
    load a resources fixture
    """
    call_command('loaddata', fixture, app_label='resources')


class Migration(migrations.Migration):
    """
    confi.gs resources initial data migration
    """
    dependencies = [
        ('resources', '0003_initial_indexes'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
