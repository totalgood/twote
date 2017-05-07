from __future__ import print_function, unicode_literals, division, absolute_import
from future import standard_library
standard_library.install_aliases()  # noqa
from builtins import *  # noqa
from future.utils import viewitems  # noqa

from twote.botornot import get_botornot
from twote.models import Label, TweetLabel, UserLabel
from twote.regexes import cre_hashtag, cre_atuser, cre_hashtag_at_end, cre_url


def is_strict(text):
    """Compute integer (0-15) indicating how useful it will be for an NLP training set

    Args:
      text (str): Tweet text

    Returns:
      int: a strictness score with 4 bits of information, MSB first:
         sum([8*contains_a_url, 4*contains_0or1_hashtags, 2*0or1_hashtag_at_end, 1*no_user_mentions]

    >>> is_strict(u"This has a url.example.com so it's not fully #strict")
    3
    >>> is_strict(u"This has a #hasher in middle but no url and has hash at #end.")
    4
    >>> is_strict(u"This has an ending #hasher.")
    15
    >>> is_strict(u"This has two ending #hasher #hashers.")
    4
    >>> is_strict(u"I still don't understand why people don't f'n follow back. I promise you won't lose your ego! #sarcasm")
    7
    """
    if not isinstance(text, (str, basestring, unicode)) or not len(text) > 2:
        return 0
    is_strict = 0

    num_hashtags = len(cre_hashtag.findall(text))
    num_atmentions = len(cre_atuser.findall(text))
    num_urls = len(cre_url.findall(text))

    is_strict += 8 * int(num_urls == 0)
    is_strict += 4 * int(num_hashtags in (0, 1))
    is_strict += 2 * int(((num_hashtags == 1 and bool(cre_hashtag_at_end.match(text))) or (num_hashtags == 0)) and
                     num_hashtags in (0, 1))
    is_strict += int(num_atmentions in (0, 1))

    return is_strict


def label_tweet(tweet):
    # tweet_id = int(tweet_id)
    is_bot, js = get_botornot(tweet.user.screen_name)
    for k, v in viewitems(js['categories']):
        name = 'botornot_' + (k[:-15] if k.endswith('_classification') else k.strip().lower())
        label, created = Label.objects.get_or_create(name=name)
        tweet_label = TweetLabel.objects.create(tweet=tweet, label=label, score=v)
    return tweet_label


def label_user(user, refresh=False):
    # tweet_id = int(tweet_id)
    is_bot, js = get_botornot('@' + user.screen_name)
    if is_bot is None or 'score' not in js:
        return [('botornot_score', None)]
    name = 'botornot_score'
    label, created = Label.objects.get_or_create(name=name)
    user_label, created = UserLabel.objects.get_or_create(user=user, label=label)
    if created or refresh:
        user_label.score = js['score']
        user_label.save()
        user.is_bot = user_label.score
        user.save()
    for k, v in viewitems(js['categories']):
        if not isinstance(v, (float, int)):
            continue
        name = 'botornot_' + (k[:-15] if k.endswith('_classification') else k.strip().lower())
        label, created = Label.objects.get_or_create(name=name)
        user_label, created = UserLabel.objects.get_or_create(user=user, label=label)
        if created or refresh:
            user_label.score = v
            user_label.save()
    return user.userlabel_set.values_list('label', 'score')
