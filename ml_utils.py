#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query Tweet model and save texts in space-delimitted format for machine learning training

Deprecated regex testing here (so this should be moved to a regex module on pugnlp or nlpia
Should deal with quotes within tweets, newlines, etc, to find hashtags.
>>> import re
>>> tough_text = "240,\"I hate it when people say, \"\"I am a vegetarian except for eggs.\"\"\n\nYeah, and I'm single except for a girlfriend."
>>> tough_text += " #sarcastic\",Rajanb92,0.33,\"[I, hate, it, when, people, say, ,, \"\", I, am, a, vegetarian, except, for, eggs, ., \"\""
>>> tough_text += ", Yeah, ,, and, I'm, single, except, for, a, girlfriend, ., #sarcastic]\""
>>> m = re.match(r'^[0-9]{1,9},"([^"]*""){0,5}[^"]*",[^,]+,[^,]*,"([^"]*""){0,5}[^"]*"$', tough_text)
>>> m.group()
'240,
"I hate it when people say, ""I am a vegetarian except for eggs.""\n\nYeah, and I\'m single except for a girlfriend. #sarcastic",
Rajanb92,
0.33,
"[I, hate, it, when, people, say, ,, "", I, am, a, vegetarian, except, for, eggs, ., "",
Yeah, ,, and, I\'m, single, except, for, a, girlfriend, ., #sarcastic]"'
"""
from __future__ import division, print_function, absolute_import, unicode_literals
from future import standard_library
standard_library.install_aliases()  # noqa
from builtins import *  # noqa
# bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import sys
import logging
import gzip
import re
from string import letters as LETTERS

import pandas as pd
from nltk.tokenize.casual import casual_tokenize
from tqdm import tqdm
from django.db.models.query import QuerySet

from gensim.corpora import Dictionary
from gensim.models import LsiModel, TfidfModel


try:
    from twote.models import Tweet
except ImportError:
    from openchat.models import Tweet

from twote.django_queryset_iterator import queryset_iterator


DATA_PATH = '/home/hobs/src/hackor/twote/data'
logger = logging.getLogger('loggly')
np = pd.np


def write_tokens(tokens, filename=None):
    filename = 'tokens{}{}.txt.gz'.format(filename, len(tokens)) if filename is None else filename
    with gzip.open(filename, 'w') as f:
        for line in tokens:
            f.write(((line or '') + '\n').encode('utf-8'))


def generate_tokens(filename='tokens.txt.gz', encoding='utf-8', limit=2000000):
    with gzip.open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            yield np.array(line.decode('utf-8').strip().split(' '))


def read_csv(filename):
    with gzip.open(filename, 'r') as f:
        df = pd.read_csv(f, encoding='utf-8', engine='python')
    return df


def write_csv(df, filename='tweets'):
    filename = '{}{}x{}.csv.gz'.format(*([filename] + list(df.shape)))
    df.to_csv(gzip.open(filename, 'w'), encoding='utf-8')


def setup_logging(loglevel=logging.WARN):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = '[%(levelname)s]%(funcName)s():%(lineno)d: %(message)s'
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


class FileCorpus(object):
    """   Iterable: on each iteration, return np.array of utf-8 tokens, One for each line.

    Assumes a sequence of space-delimitted tokens on each line within a gzipped file
    """
    def __init__(self, filename, dictionary=None, limit=2000000, prune_at=2000000, verbose=False):
        self.filename = filename
        self.limit = limit
        self.num_passes = 0
        self.prune_at = prune_at
        if dictionary is None:
            self.dictionary = Dictionary(tqdm(generate_tokens(filename, limit=limit), total=limit), prune_at=prune_at)
            self.num_passes += 1
            self.shape = (self.dictionary.num_docs, len(self.dictionary.dfs))
        else:
            self.dictionary = dictionary
            # TODO: make this lazier
            self.shape = (sum(1 for doc in tqdm(generate_tokens(filename, limit=self.limit))),
                          len(self.dictionary.dfs))
            if not (self.shape[0] == self.dicionary.num_docs):
                logger.warn('File {} has different number of docs ({}) than the dictionary ({}docs,{}words). Consider recompiling Dictionary.'.format(
                            self.shape[0], self.dictionary.num_docs, self.shape[1]))
            self.num_passes += 1
        self.tfidf = TfidfModel(dictionary=self.dictionary, id2word=self.dictionary)

    def iter_tokens(self):
        for i, tokens in enumerate(tqdm(generate_tokens(self.filename, limit=self.limit), total=len(self))):
            # transform tokens (strings) into a sparse vector, one at a time
            yield tokens

    def __iter__(self):
        """
        Again, __iter__ is a generator => TxtSubdirsCorpus is a streamed iterable.
        """
        for i, tokens in enumerate(tqdm(generate_tokens(self.filename, limit=self.limit), total=len(self))):
            # transform tokens (strings) into a sparse vector, one at a time
            yield self.tfidf[self.dictionary.doc2bow(tokens)]
        self.shape = (i, len(self.dictionary.dfs)) if self.shape is None else self.shape

    def __len__(self):
        if self.shape is None:
            self.shape = (sum(1 for doc in generate_tokens(self.filename, limit=self.limit)),
                          len(self.dictionary.dfs))
            self.num_passes += 1
        return self.shape[0]

    def __str__(self):
        return 'FileCorpus(filename={}) object with shape {}x{}'.format(self.filename, self.shape[0], self.shape[1])

    def __repr__(self):
        return self.__str__()


def return_none(*args, **kwargs):
    return None


def get_len(it):
    return getattr(it, 'count', getattr(it, '__len__', return_none))()


def bits2letters(bits):
    """ Decypher clever binary usernames

    >>> bits2str('011011100110010101110100')
    'net'
    >>> chr(int('01101110', 2)) + chr(int('01100101', 2))  + chr(int('01110100',2))
    'net'
    """
    bitchrs = re.findall('[\b]?[01]{5,8}[\b]?', bits)
    letters64 = LETTERS + '*' * (64 - len(LETTERS))
    letters32 = LETTERS + '*' * (32 - len(LETTERS))

    ans = ''
    for b in bitchrs:
        i = int(b, 2)
        if len(b) > 6:
            ans += chr(i)
        elif len(b) > 5:
            ans += letters64[i]
        else:
            ans += letters32[i]
    return ans


def write_tweets(tweets, f, total=None, donepks=None, eol='\n'):
    donepks = set() if donepks is None else set(donepks)
    morepks = set()
    total = get_len(tweets) if total is None else total
    tweets = queryset_iterator(tweets) if isinstance(tweets, QuerySet) else tweets

    for t in tqdm(tweets, total=total):
        if isinstance(t, (int, str)):
            if t is -1:
                continue
            try:
                t = Tweet.objects.get(pk=t)
            except:
                Tweet.DoesNotExist
                logger.warn('Tweet(pk={}).DoesNotExist'.format(t))
                continue
        if isinstance(t, Tweet):
            # TODO: make this a namedtuple or dict
            t = (t.pk,                                  # 0
                 getattr(t, 'created_date', None),      # 1
                 t.in_reply_to,                         # 2
                 getattr(t.user, 'location', '*'),     # 3
                 getattr(t.user, 'is_bot', None),       # 4
                 t.is_strict,                           # 5
                 getattr(t.user, 'screen_name', '*'),  # 6
                 t.text or '*')                                # 7
        if not (isinstance(t, (tuple, list)) and len(t) == 8):
            continue
        pk = t[0]                                     # 0 pk            int
        created_date = (t[1].isoformat()
            if hasattr(t[1], 'isoformat') else '*')   # 1 created_date  datetime -> str w/o whitespace
        in_reply_to = getattr(t[2], 'pk', -1) or -1   # 2 in_reply_to   int
        # TODO: compose a string from tweet.place.city, state, country when available
        loc = re.sub('\s', '*', t[3])                 # 3 location      str without whitespace
        is_bot = float(t[4] or -1)                    # 4 is_bot        float
        is_strict = int(float(t[5] or -1))            # 5 is_strict     in
        user = re.sub('\s', '*', t[6])                # 6 user          str without whitespace
        text = t[7].replace(eol, ' ')        # 7 text          str without EOLs

        line = '{:<12} {:<26} {:<12} {:<32} {:<4} {:<4} {:<32} '.format(pk, created_date, in_reply_to, loc, is_bot, is_strict, user)
        line += ' '.join(casual_tokenize(text or '', reduce_len=True, strip_handles=False))
        line += eol
        line = line.encode('utf-8')
        f.write(line)

        donepks.add(pk)
        if in_reply_to is not None and in_reply_to not in donepks and in_reply_to >= 0:
            morepks.add(in_reply_to)

    return donepks, morepks


def save_tweet_dialogs(tweets=None, total=None, opener=gzip.open, depth=16, filename='save_tweet_dialogs.txt.gz',
                       min_strictness=15, min_botness=0, max_botness=.45):
    if tweets is None:
        tweets = (Tweet.objects.filter(is_strict__gte=min_strictness, user__is_bot__gte=min_botness, user__is_bot__lte=max_botness) |
                  Tweet.objects.filter(is_strict__gte=min_strictness, in_reply_to__is_strict__gte=min_strictness))
        total = total or tweets.count()
        # tweets = tweets.values_list(*
        #     'pk in_reply_to user_location user__is_bot is_strict user__screen_name text'.split())
    with opener(filename, 'wb') as f:
        donepks = set()
        morepks = tweets
        total = get_len(morepks)
        i = 0
        while total > 0 and i < depth:
            donepks, morepks = write_tweets(tweets=morepks, f=f, donepks=donepks, total=total)
            i += 1
    return donepks, morepks


def save_large_corpus(tweets=None, strictness=10, opener=open, filename='pk_user_isbot_isstrict_text.txt'):
    tweets = Tweet.objects.filter(is_strict__gte=strictness) if tweets is None else tweets
    N = tweets.count()
    tweets = queryset_iterator(tweets.values_list('pk', 'user__screen_name', 'user__is_bot', 'is_strict', 'text'))
    with opener(filename, 'wb') as f:
        for t in tqdm(tweets, total=N):
            s = t[-1].replace('\r', ' ').replace('\n', ' ')
            f.write(('{} {:.2f} {} {}: '.format(t[0], float(t[2] or -1), int(t[3] or -1), t[1]) +
                    ' '.join(casual_tokenize(s or '',
                                             reduce_len=True,
                                             strip_handles=False)) + '\n').encode('utf-8'))


def save_corpus(strictness=10, filename='botness_text', reduce_len=True, strip_handles=True, is_bot__isnull=False):
    qs = Tweet.objects.filter(is_strict__gte=strictness, user__is_bot__isnull=is_bot__isnull)
    tweets = list(qs.values_list('pk', 'user__screen_name', 'user__is_bot', 'text'))
    pk, user, is_bot, text = zip(*tweets)
    tweets = pd.DataFrame(index=pk)
    tweets['user'] = user
    tweets['is_bot'] = np.array(is_bot).astype(float)
    tweets['text'] = np.array([s.replace('\r', ' ').replace('\n', ' ') for s in text])
    tweets.to_csv(gzip.open(filename + '.csv.gz', 'w'), encoding='utf-8')
    with gzip.open(filename + '_tokens.txt.gz', 'w') as f:
        for text in tweets.text:
            f.write((' '.join(casual_tokenize(s or '',
                                              reduce_len=reduce_len,
                                              strip_handles=strip_handles)) + '\n').encode('utf-8'))
    return tweets.shape


def lsi_model(filename='tokens.txt.gz', limit=5000000):
    corpus = FileCorpus(filename, limit=limit)
    num_docs = len(corpus)

    lsi = LsiModel(corpus, num_topics=100, id2word=corpus.dictionary, extra_samples=100, power_iters=2)
    lsi.save(DATA_PATH + '/lsi{}x{}x{}.saved'.format(num_docs, lsi.num_topics, lsi.num_terms))
    return lsi


def topic_vectors(lsi=None, corpus='tokens.txt.gz', filename='topics.csv.gz', limit=4000000):
    lsi = LsiModel.load(lsi) if isinstance(lsi, basestring) else lsi
    corpus = FileCorpus(corpus, limit=limit) if isinstance(corpus, basestring) else corpus
    df = np.zeros((corpus.shape[0], lsi.num_topics))
    badrows = []
    for i, doc in enumerate(corpus):
        keys, values = zip(*sorted(lsi[doc]))
        # if not i % 100000:
        #     print(keys)
        #     print(values)
        #     print(len(keys), len(values))
        if len(values) == lsi.num_topics:
            df[i, :] = values
        else:
            badrows += [i]
            logger.warn('Invalid LSI vector: {} (len {})'.format(keys, len(keys)))
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!!!!!!!!!!")
            print(keys)
            print(values)
            print(len(keys), len(values))
            for k, v in zip(keys, values):
                df[i, k] = v
    pd.DataFrame(df).to_csv(gzip.open('topics.csv.gz', 'w'), encoding='utf-8')
    return badrows
    # topics = lsi[tfidf[bows]]
    # topics = pd.DataFrame([dict(d) for d in topics], index=tweets.index, columns=range(80))


def write_cole(tweets, tokens_filename):
    with gzip.open('id_botness_tokens.txt.gz', 'w') as f:
        for i, ((pk, row), toks) in tqdm(enumerate(zip(tweets.iterrows(), generate_tokens(tokens_filename, limit=4000000)))):
            if pd.isnull(row['is_bot']):
                continue
            print(i, pk)
            print(float(row['is_bot']))
            print(toks)
            f.write('{:d} {:0.2f} {}'.format(i, float(row['is_bot']), ' '.join(toks).encode('utf-8')))


def cleanup_csv(filename):
    re_line = re.compile(r'^[0-9]{1,9},"([^"]*""){0,5}[^"]*",[^,]+,[^,]*,"([^"]*""){0,5}[^"]*"$')
    multiline = ''
    f = gzip.open(filename)
    while f:
        for line in f:
            for i in range(256):
                if re_line.match(multiline):
                    break
                print('incomplete: {}')
