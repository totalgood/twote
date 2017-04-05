# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0012_auto_20170330_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLabel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=None, help_text='Score float value between 0 and 1 (like probability).', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='label',
            name='score',
        ),
        migrations.AddField(
            model_name='tweetlabel',
            name='score',
            field=models.FloatField(default=None, help_text='Score float value between 0 and 1 (like probability).', null=True),
        ),
        migrations.AddField(
            model_name='userlabel',
            name='label',
            field=models.ForeignKey(to='twote.Label'),
        ),
        migrations.AddField(
            model_name='userlabel',
            name='user',
            field=models.ForeignKey(to='twote.User'),
        ),
    ]
