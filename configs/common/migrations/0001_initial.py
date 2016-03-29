import common.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
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
                    'name', common.fields.TagField(
                        max_length=64,
                        unique=True)
                ),
            ],
        ),
    ]
