#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Label all users' tweets with the BotOrNot scores for the sending User

>>> cre_hashtag_at_end.match("There's a hashtag at the end #here. ")
<_sre.SRE_Match at ...>
>>> cre_hashtag_at_end.match("There's a #hashtag at the end #here  --?--  ")
<_sre.SRE_Match at ...>
>>> cre_hashtag_at_end.match("There's a #hashtag at the end #here  -- ? --  ")
<_sre.SRE_Match at ...>
>>> cre_hashtag_at_end.match("There's not a #hashtag at the end in this one  -- ? --  ")
>>> cre_hashtag_at_end.match("There's not a #hashtag at the end or this #1")
>>> cre_hashtag_at_end.match("There's is a smart #hashtag at at the end of tweets about #ai")
<_sre.SRE_Match at ...>
"""
from __future__ import print_function, unicode_literals, division, absolute_import
from future import standard_library
standard_library.install_aliases()  # noqa
from builtins import *  # noqa
from future.utils import viewitems  # noqa

import sys
import os
import argparse
import logging
import time

from tqdm import tqdm  # noqa

from pugnlp.regexes import cre_url  # noqa

from twote.django_queryset_iterator import queryset_iterator
from twote.botornot import get_botornot

from twote.models import Tweet, User, Label, TweetLabel, UserLabel

try:
    from twote import __version__
except ImportError:
    __version__ = "0.0.0"


if __name__ == "__main__" or not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openchat.settings")
    from django.conf import settings  # noqa


__author__ = "Total Good"
__copyright__ = "Total Good"
__license__ = "mit"

logger = logging.getLogger(__name__)
loggly = logging.getLogger('loggly')


from twote.labelers import label_tweet, label_user


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Labels tweets for their 'strictness' (how valuable they are for ML training).")
    parser.add_argument(
        '--version',
        action='version',
        version='twote {ver}'.format(ver=__version__))
    parser.add_argument(
        '-l',
        '--limit',
        dest="limit",
        default=1000,
        help="Limit number of tweets processed.",
        type=int)
    parser.add_argument(
        '--start',
        dest="start",
        default=0,
        help="Which record to start processing on (enables skipping previously processed records).",
        type=int)
    parser.add_argument(
        '--sleep',
        dest="sleep",
        default=1000,
        help="Sleep ms between botornot checks.",
        type=int)
    parser.add_argument(
        '-b',
        '--batch',
        dest="batch",
        default=1000,
        help="Number of tweets per batch updated in the database.",
        type=int)
    parser.add_argument(
        '--strictness',
        dest="strictness",
        default=15,
        help="Strictness level to filter tweets by.",
        type=int)
    parser.add_argument(
        '--min_tweets',
        dest="min_tweets",
        default=10,
        help="Minimum number of strict tweets a user must have in our DB before they are labeled.",
        type=int)
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        default=logging.WARN,
        const=logging.INFO)
    parser.add_argument(
        '-r',
        '--refresh',
        dest="refresh",
        help="Recompute/refresh existing strictness scores. Otherwise only empty (None) records will be processed",
        action='store_true',
        default=False)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        default=logging.WARN,
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel=logging.WARN):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def no_tqdm(*args, **kwargs):
    return args[0] if len(args) else kwargs['qs']


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    global tqdm
    args = parse_args(args)
    setup_logging(args.loglevel)
    print(args)

    if args.loglevel < logging.WARN:
        pbar = no_tqdm  # noqa
    else:
        pbar = tqdm

    labeled_user_pks = set(list(User.objects.filter(userlabel__isnull=False).values_list('pk', flat=True).distinct()))
    qs = Tweet.objects.filter(is_strict__gte=args.strictness).exclude(user__pk__in=labeled_user_pks)
    limit = min(args.limit, qs.count() - args.start)

    print("Labeling {} tweets starting at tweet #{}".format(limit, args.start))

    for i, tweet in pbar(enumerate(queryset_iterator(qs, batchsize=args.batch)), total=limit):
        if i < args.start:
            continue
        if tweet.user.pk not in labeled_user_pks:
            scores = label_user(tweet.user)
            labeled_user_pks.add(tweet.user.pk)
        else:
            scores = tweet.user.userlabel_set.filter(label__name='botornot_score').values_list('score', flat=True)
        logger.debug(u"{:6.1f}% {}: {}".format(100. * i / float(limit), scores[0] if scores else None, tweet.text))
        # batch += [tweet]
        if i >= args.limit:
            break
        if i and not (i % args.batch):
            # Tweet.batch_update(tweet)
            # batch = []
            logger.info(u"{:6.1f}% {}: {}".format(100. * i / limit, tweet.is_strict, tweet.text))
        label_tweet(tweet)
        time.sleep(args.sleep / 1000.)

    logger.info(u"Finished labeling {} tweets".format(i))


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == '__main__':
    run()
