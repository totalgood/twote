# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0011_tweet_source_bot'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamedTestTweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('id_str', models.CharField(default='', max_length=256, db_index=True)),
                ('source', models.CharField(max_length=256, null=True, blank=True)),
                ('text', models.CharField(max_length=256, null=True, blank=True)),
                ('location', models.CharField(max_length=256, null=True, blank=True)),
                ('favorite_count', models.IntegerField(default=-1, null=True)),
                ('user', models.ForeignKey(blank=True, to='twote.User', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='outgoingconfig',
            name='ignore_users',
            field=django.contrib.postgres.fields.ArrayField(default=[], base_field=models.BigIntegerField(), size=None),
            preserve_default=False,
        ),
    ]
