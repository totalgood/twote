# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0014_user_label'),
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
    ]
