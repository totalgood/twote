# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0013_auto_20170405_0607'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='features',
            field=django.contrib.postgres.fields.ArrayField(null=True, base_field=models.FloatField(), size=None),
        ),
        migrations.AddField(
            model_name='user',
            name='is_bot',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='label',
            field=models.ManyToManyField(to='twote.Label', through='twote.UserLabel'),
        ),
    ]
