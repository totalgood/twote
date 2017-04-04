#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constants and discovered values, like path to current installation of pug-nlp."""
from __future__ import division, print_function, absolute_import, unicode_literals
from builtins import (  # noqa
    bytes, dict, int, list, object, range, str,
    ascii, chr, hex, input, next, oct, open,
    pow, round, super,
    filter, map, zip)

import json
import requests

import tweepy

from twote.secrets import opntwt


auth = tweepy.OAuthHandler(opntwt['CONSUMER_KEY'], opntwt['CONSUMER_SECRET'])
auth.set_access_token(opntwt['ACCESS_TOKEN'], opntwt['ACCESS_TOKEN_SECRET'])
twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


def get_botornot(screen_name):
    screen_name = screen_name if screen_name[0] == '@' else '@' + screen_name
    user_timeline = twitter_api.user_timeline(screen_name, count=200)
    user_data = user_timeline[0]['user'] if user_timeline else twitter_api.get_user(screen_name)
    search_results = twitter_api.search(screen_name, count=100)
    mentions = search_results['statuses']
    post_body = {'content': user_timeline + mentions,
                 'meta': {
                     'user_id': user_data['id_str'],
                     'screen_name': screen_name,
                     },
                 }
    bon_url = 'http://truthy.indiana.edu/botornot/api/1/check_account'
    bon_response = requests.post(bon_url, data=json.dumps(post_body))
    bon_response.status_code
    js = bon_response.json()
    return js.get('score', None), js
