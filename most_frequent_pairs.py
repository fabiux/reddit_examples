# -*- coding: utf-8 -*-
"""
This is an example to show how to find most frequent (stemmed) words on titles of
latest Reddit posts, for a given topic.
Post are stored in a local MongoDB collection (see scan_reddit_topics.py).

Author: Fabio Pani <fabiux AT fabiopani DOT com>
License: see LICENSE
"""
from nltk.stem.lancaster import LancasterStemmer  # FIXME try another stemmer
from stop_words import get_stop_words
from re import compile
from pymongo import MongoClient
from operator import itemgetter
from time import time

topics = {'t5_2r3gv': 'MachineLearning',
          't5_31xmi': 'textdatamining',
          't5_2s9be': 'bigdata'}

fromtime = int(time()) - (86400 * 28)  # 28 days back


def most_frequent_pairs(topic_id):
    """
    Compute most frequent stemmed word pairs for the specified Reddit topic id.
    Skip stop words.
    :param topic_id: topic id (subreddit_id)
    :type topic_id: str
    :return: sorted list of most frequent stemmed word pairs (from most to less frequent)
    """
    topwords = dict()  # dict used to count frequency for each stemmed word
    articles = MongoClient().reddit.articles
    res = articles.find({'subreddit_id': topic_id, 'created_utc': {'$gt': fromtime}},
                        {'_id': 0, 'title': 1})
    for art in res:
        words = r.sub(' ', art['title'].lower()).split()  # alphachars only
        words = [st.stem(w) for w in words if (w not in stop_words) and (len(w) > 1)]  # stemmed words
        for word in words:
            if len(word) > 2:  # stemmed words longer than 2 chars only
                if topwords.get(word) is None:
                    topwords[word] = 1
                else:
                    topwords[word] += 1

    # keep words with frequency >= 3
    for k, v in topwords.items():
        if v < 3:
            del topwords[k]

    # create a set of topwords for each article that contains at least one
    matrix = dict()
    for word in topwords:
        res = articles.find({'$text': {'$search': word}}, {'_id': 0, 'id_reddit': 1})  # full text search
        for item in res:
            if matrix.get(item['id_reddit']) is None:
                matrix[item['id_reddit']] = set([])  # create initial empty set
            matrix[item['id_reddit']].add(word)

    # keep sets with cardinality >= 2
    for k, v in matrix.items():
        if len(v) < 2:
            del matrix[k]

    # count frequency for all possible pairs of topwords
    pairs = dict()
    for v in matrix.values():
        v = sorted(v)
        for i in range(len(v) - 1):
            for j in range(i + 1, len(v)):
                idx = v[i], v[j]
                if pairs.get(idx) is None:
                    pairs[idx] = 1
                else:
                    pairs[idx] += 1

    return sorted(pairs.items(), key=itemgetter(1), reverse=True)  # sorted from most to less frequent

if __name__ == '__main__':
    stop_words = get_stop_words('english')  # stop words to skip
    st = LancasterStemmer()
    r = compile('[^a-z_]')

    for topic in topics.keys():
        print topics[topic]
        print most_frequent_pairs(topic)
