#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constants and discovered values, like path to current installation of pug-nlp.

>>> get_botornot('@opntwt')
(0.83, {u'categories': {u'content_classification': 0.7,
  u'friend_classification': 0.7931471336512232,
  u'languageagnostic_classification': 0.7878337355686594,
  u'network_classification': 0.8031867345231665,
  u'sentiment_classification': 0.71,
  u'temporal_classification': 0.7879518434631023,
  u'user_classification': 0.7838863574969136},
 u'meta': {u'screen_name': u'@opntwt', u'user_id': u'848688179897024512'},
 u'score': 0.83})
>>> get_botornot('@hobsonlane')
(0.25, {u'categories': {u'content_classification': 0.29,
  u'friend_classification': 0.23,
  u'languageagnostic_classification': 0.21,
  u'network_classification': 0.18,
  u'sentiment_classification': 0.17,
  u'temporal_classification': 0.29,
  u'user_classification': 0.1},
 u'meta': {u'screen_name': u'@hobsonlane', u'user_id': u'59275999'},
 u'score': 0.25})
"""
from __future__ import division, print_function, absolute_import, unicode_literals
from builtins import (  # noqa
    bytes, dict, int, list, object, range, str,
    ascii, chr, hex, input, next, oct, open,
    pow, round, super,
    filter, map, zip)

import json
import requests

import tweepy

from twote.secrets import goodtotal  # opntwt
from tweepy import TweepError


auth = tweepy.OAuthHandler(goodtotal['CONSUMER_KEY'], goodtotal['CONSUMER_SECRET'])
auth.set_access_token(goodtotal['ACCESS_TOKEN'], goodtotal['ACCESS_TOKEN_SECRET'])
twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


def get_botornot(screen_name):
    screen_name = screen_name if screen_name[0] == '@' else '@' + screen_name
    try:
        user_timeline = twitter_api.user_timeline(screen_name, count=200)
    except TweepError:
        print('User {} timeline not found?'.format(screen_name))
        user_timeline = None
    try:
        user_data = user_timeline[0]['user'] if user_timeline else twitter_api.get_user(screen_name)
    except TweepError:
        print('User {} profile not found?'.format(screen_name))
        return None, {}
    search_results = twitter_api.search(screen_name, count=100)
    mentions = search_results['statuses']
    post_body = {'content': list(user_timeline or []) + mentions,
                 'meta': {
                     'user_id': user_data['id_str'],
                     'screen_name': screen_name,
                     },
                 }
    bon_url = 'http://truthy.indiana.edu/botornot/api/1/check_account'
    bon_response = requests.post(bon_url, data=json.dumps(post_body))
    js = {}
    if bon_response.status_code == 200 or bon_response.ok:
        js = bon_response.json()
    return js.get('score', None), js
