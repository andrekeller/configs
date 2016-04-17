"""
confi.gs common migrations
"""
# django
from django.db import migrations, models
# confi.gs
from ..fields import TagField


class Migration(migrations.Migration):
    """
    confi.gs common initial model migration
    """
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
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
                (
                    'notes', models.TextField(
                        blank=True,
                        null=True
                    )
                ),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
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
                    'name', TagField(
                        max_length=64,
                        unique=True
                    )
                ),
            ],
        ),
    ]
