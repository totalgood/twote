#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.cfg:

    console_scripts =
     fibonacci = twote.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!

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
from __future__ import division, print_function, absolute_import
# from builtins import int, round, str
from future import standard_library
standard_library.install_aliases()
from builtins import object  # NOQA

import sys  # noqa
import gc  # noqa
import os  # noqa
import re  # noqa
import argparse  # noqa
import logging  # noqa

from tqdm import tqdm  # noqa

from pugnlp.regexes import cre_url  # noqa

# from twote import __version__  # noqa
from twote.models import Tweet  # noqa


if __name__ == "__main__" or not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openchat.settings")
    from django.conf import settings  # noqa

try:
    from twote import __version__
except:
    __version__ = "0.0.0"

__author__ = "Total Good"
__copyright__ = "Total Good"
__license__ = "mit"

logger = logging.getLogger(__name__)
loggly = logging.getLogger('loggly')


re_hashtag = r'\b#[A-Za-z]{2,32}\b'
cre_hashtag = re.compile(re_hashtag)
re_hashtag_at_end = r'.*\s([#][A-Za-z]{2,32})\s*[.?!-=\s]{0,8}\s*$'
cre_hashtag_at_end = re.compile(re_hashtag_at_end)


def is_strict(text):
    """Fibonacci example function

    Args:
      text (str): Tweet text

    Returns:
      int: a class of strictness, 0 meaning contains a URL or more than 1 hashtag, or hashtag isn't at end

    >>> is_strict("This has a url.example.com so it's not strict")
    0
    >>> is_strict("This has a #hasher in middle.")
    0
    >>> is_strict("This has an ending #hasher.")
    1
    >>> is_strict("This has two ending #hasher #hashers.")
    0
    """
    is_strict = int(not cre_url.findall(text))
    num_hashtags = len(cre_hashtag.findall(text))
    is_strict = is_strict + int(num_hashtags in (0, 1))
    is_strict += int((num_hashtags == 1 and bool(cre_hashtag_at_end.match(text))) or num_hashtags == 0)
    return is_strict


def label_tweet(tweet):
    # tweet_id = int(tweet_id)
    tweet.is_strict = int(is_strict(tweet.text))
    return tweet


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
        '-b',
        '--batch',
        dest="batch",
        default=1,
        help="Number of tweets per batch updated in the database.",
        type=int)
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def queryset_iterator(qs, batchsize=500, gc_collect=True):
    iterator = qs.values_list('pk', flat=True).order_by('pk').distinct().iterator()
    eof = False
    while not eof:
        primary_key_buffer = []
        try:
            while len(primary_key_buffer) < batchsize:
                primary_key_buffer.append(iterator.next())
        except StopIteration:
            eof = True
        for obj in qs.filter(pk__in=primary_key_buffer).order_by('pk').iterator():
            yield obj
        if gc_collect:
            gc.collect()


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    print(args)
    logger.info(args)
    for i, tweet in tqdm(enumerate(queryset_iterator(Tweet.objects.iterator())), total=args.limit):
        print(i, tweet)
        tweet.is_strict = is_strict(tweet.text)
        tweet.save(update_fields=['is_strict'])
        # batch += [tweet]
        if i >= args.limit:
            break
        if not i % args.batch and not i:
            # Tweet.batch_update(tweet)
            # batch = []
            logger.info(u"{}: {}".format(tweet.is_strict, tweet.text))
        else:
            logger.info(u"{}: {}".format(tweet.is_strict, tweet.text))

    logger.info("Finished labeling {} tweets".format(i))


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == '__main__':
    run()
