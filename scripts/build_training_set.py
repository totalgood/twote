from __future__ import division, print_function, absolute_import
# from builtins import int, round, str
from future import standard_library
standard_library.install_aliases()  # noqa
from builtins import object  # noqa

from seaborn import plt

from collections import Counter
import pandas as pd

from twote.models import Tweet

from nltk.tokenize import SExprTokenizer  # noqa parenthesized expressions
from nltk.tokenize import TreebankWordTokenizer, MWETokenizer, StanfordTokenizer  # noqa


strict_counts = Counter(Tweet.objects.values_list('is_strict', flat=True))
pd.Series(strict_counts).plot(kind='bar')
plt.show()

columns = ['pk', 'tags']
hashes = list(Tweet.objects.filter(is_strict=15).values('tags').exclude(tags__contains=' ').values_list(*columns))
df = pd.DataFrame(hashes, columns=columns)
df = df.set_index('pk', drop=True)
tag_counts = df.tags.value_counts()
tag_counts.sort_values(inplace=True, ascending=False)

"""
>>> tag_counts.head(20)
                    3258891
quote                 50116
bot                   31043
Bot                   29158
sad                    9303
winning                7208
knowledge              6902
BOT                    6095
sarcasm                5071
QUOTE                  4070
life                   3792
thankful               3743
happy                  3236
lol                    3185
gratitude              2834
Sad                    2628
Thankful               2500
nice                   2387
mondaymotivation       2045
awesome                1785
Name: tags, dtype: int64
"""


def mask_tags(tags,
              exact_tags=['happy', 'awesome', 'thankful', 'gratitude', 'ecstatic', 'bliss', 'motivation', 'peace', 'excited', 'joy', 'happiness'],
              in_tags=['happybirthday']):
    """Return a boolean numpy array (mask) that is True if any true_tags are among the lists of tags in tags Series"""
    exact_tags = [exact_tags] if isinstance(exact_tags, basestring) else exact_tags
    mask = pd.np.array([True] * len(tags))
    tags = pd.Series(tags, name='tag')
    tags = tags.str.lower()
    split_tags = tags.str.lower().str.split()
    for et in in_tags:
        mask |= split_tags.apply(lambda row: et in row)
    for it in in_tags:
        mask |= tags.apply(lambda row: it in row)
    return mask
