# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0015_user_is_bot'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='features',
            field=django.contrib.postgres.fields.ArrayField(null=True, base_field=models.FloatField(), size=None),
        ),
    ]
