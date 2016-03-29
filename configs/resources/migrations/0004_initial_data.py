from django.db import migrations
from django.core.management import call_command

fixture = 'configs_defaults'


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label='resources')


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0003_initial_indexes'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
