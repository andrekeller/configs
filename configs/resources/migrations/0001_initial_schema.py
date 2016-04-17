"""
confi.gs resources initial database schema
"""
# django
from django.contrib.postgres.fields.hstore import HStoreField
from django.contrib.postgres.operations import HStoreExtension
from django.db import migrations, models
from django.db.models.deletion import CASCADE
from django.db.models.deletion import SET_DEFAULT
# 3rd-party
from tagging.fields import TagField
# confi.gs
from cidrfield.fields import CidrField
from cidrfield.validators import validate_network
from common.models.mixins import ValidateModelMixin


class Migration(migrations.Migration):
    """
    confi.gs resource initial migration.
    """
    initial = True

    dependencies = [
    ]

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name='Domain',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name', models.CharField(
                        max_length=255
                    )
                ),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name', models.CharField(
                        max_length=255
                    )
                ),
                (
                    'encdata', HStoreField(
                        blank=True,
                        null=True
                    )
                ),
                (
                    'tags', TagField(
                        blank=True,
                        max_length=255
                    )
                ),
                (
                    'domain', models.ForeignKey(
                        on_delete=CASCADE,
                        to='resources.Domain'
                    )
                ),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'network', CidrField(
                        validators=[validate_network]
                    )
                ),
                (
                    'description', models.TextField(
                        blank=True,
                        null=True
                    )
                ),
                (
                    'use_reserved_addresses', models.BooleanField(
                        default=False
                    )
                ),
                (
                    'tags', TagField(
                        blank=True,
                        max_length=255
                    )
                ),
                (
                    'host', models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=CASCADE,
                        to='resources.Host'
                    )
                ),
            ],
            options={
                'ordering': ['network'],
            },
        ),
        migrations.CreateModel(
            name='ResourceStatus',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name', models.CharField(
                        max_length=50,
                        unique=True
                    )
                ),
            ],
            bases=(
                ValidateModelMixin,
                models.Model
            ),
        ),
        migrations.CreateModel(
            name='Vlan',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'vlan_id', models.IntegerField()
                ),
                (
                    'vlan_name', models.CharField(
                        max_length=255)
                ),
            ],
            options={
                'ordering': ['vlan_id'],
            },
            bases=(
                ValidateModelMixin,
                models.Model
            ),
        ),
        migrations.CreateModel(
            name='Vrf',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name', models.CharField(
                        max_length=255,
                        unique=True
                    )
                ),
            ],
            bases=(
                ValidateModelMixin,
                models.Model
            ),
        ),
        migrations.AddField(
            model_name='vlan',
            name='vrf',
            field=models.ForeignKey(
                default=1,
                on_delete=SET_DEFAULT,
                to='resources.Vrf'
            ),
        ),
        migrations.AddField(
            model_name='network',
            name='status',
            field=models.ForeignKey(
                default=1,
                on_delete=CASCADE,
                to='resources.ResourceStatus'
            ),
        ),
        migrations.AddField(
            model_name='network',
            name='vlan',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=CASCADE,
                to='resources.Vlan'
            ),
        ),
        migrations.AddField(
            model_name='network',
            name='vrf',
            field=models.ForeignKey(
                default=1,
                on_delete=CASCADE,
                to='resources.Vrf'
            ),
        ),
        migrations.AlterUniqueTogether(
            name='vlan',
            unique_together={('vlan_id', 'vrf')},
        ),
        migrations.AlterUniqueTogether(
            name='network',
            unique_together={('network', 'vrf')},
        ),
        migrations.AlterUniqueTogether(
            name='host',
            unique_together={('name', 'domain')},
        ),
    ]
