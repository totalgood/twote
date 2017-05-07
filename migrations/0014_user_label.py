# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0013_auto_20170405_0607'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='label',
            field=models.ManyToManyField(to='twote.Label', through='twote.UserLabel'),
        ),
    ]
