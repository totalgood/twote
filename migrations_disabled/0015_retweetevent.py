# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0014_auto_20170409_2142'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetweetEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('start', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('creator', models.CharField(max_length=100, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'twote_retweetevent',
            },
        ),
    ]
