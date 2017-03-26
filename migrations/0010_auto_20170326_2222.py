# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twote', '0009_outgoingconfig_outgoingtweet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(default='')),
                ('score', models.FloatField(default=None, help_text='Score float value between 0 and 1 (like probability).', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TweetLabel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.ForeignKey(to='twote.Label')),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='contains_url',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='is_strict',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='tweetlabel',
            name='tweet',
            field=models.ForeignKey(to='twote.Tweet'),
        ),
        migrations.AddField(
            model_name='tweet',
            name='label',
            field=models.ManyToManyField(to='twote.Label', through='twote.TweetLabel'),
        ),
    ]
