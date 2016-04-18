"""
confi.gs networkgroup migrations
"""
from django.db import migrations, models
from django.db.models.deletion import SET_NULL


class Migration(migrations.Migration):
    """
    confi.gs migration to add initial support for network groups
    """

    dependencies = [
        ('resources', '0004_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkGroup',
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
                        unique=True,
                    )
                ),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='network',
            name='group',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=SET_NULL,
                to='resources.NetworkGroup'
            ),
        ),
    ]
