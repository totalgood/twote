# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0014_user_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_bot',
            field=models.FloatField(default=None, null=True),
        ),
    ]
