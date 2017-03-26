# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0010_auto_20170326_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='source_bot',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
