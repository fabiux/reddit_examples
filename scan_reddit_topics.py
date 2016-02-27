# -*- coding: utf-8 -*-
"""
Scan topics and get new posts at Reddit.

Author: Fabio Pani <fabiux AT fabiopani DOT com>
License: see LICENSE
"""
from pymongo import MongoClient
from urllib2 import Request, build_opener
from json import loads
from time import sleep

topics = ['MachineLearning', 'bigdata', 'textdatamining']
articles = MongoClient().reddit.articles


def get_remote_url(url, timeout=30):
    """
    Download a remote resource.
    :param url: resource URL
    :type url: str
    :param timeout: timeout (seconds)
    :type timeout: int
    :return: resource content or None if errors
    """
    try:
        request = Request(url)
        request.add_header('User-Agent', 'RSS reader [see https://github.com/fabiux/reddit_examples]')
        opener = build_opener()
        respdata = opener.open(request, timeout=timeout)
        if respdata.code == 200:
            return respdata.read()
        else:
            return None
    except Exception:
        return None


if __name__ == '__main__':
    for topic in topics:
        arts = get_remote_url('https://www.reddit.com/r/' + topic + '/new/.json')
        if arts is not None:
            j = loads(arts)
            for article in j['data']['children']:
                newart = dict()
                newart['id_reddit'] = article['data']['id']
                newart['subreddit'] = article['data']['subreddit']
                newart['subreddit_id'] = article['data']['subreddit_id']
                newart['domain'] = article['data']['domain']
                newart['selftext'] = article['data']['selftext']
                newart['domain'] = article['data']['domain']
                newart['author'] = article['data']['author']
                newart['permalink'] = article['data']['permalink']
                newart['url'] = article['data']['url']
                newart['created_utc'] = article['data']['created_utc']
                newart['title'] = article['data']['title']
                try:
                    articles.insert_one(newart)
                except Exception:  # skip if a post already exists
                    pass
        sleep(60)
