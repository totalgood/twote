#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query Tweet model and save texts for strictness >=13 tweets in space-delimitted format for machine learning training

"""
from __future__ import division, print_function, absolute_import, unicode_literals
from future import standard_library
standard_library.install_aliases()  # noqa
from builtins import *  # noqa

from twote.tweet_utils import *

strictness = 15
# tweets = (Tweet.objects.filter(is_strict__gte=strictness, user__is_bot__gte=0, user__is_bot__lte=.45) |
#                   Tweet.objects.filter(is_strict__gte=strictness, in_reply_to__is_strict__gte=strictness))
qs = Tweet.objects.filter(is_strict__gte=strictness, user__is_bot__gte=0, user__is_bot__lte=.5)
save_tweet_dialogs(qs, depth=32)
