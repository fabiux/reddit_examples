# -*- coding: utf-8 -*-
"""
Create MongoDB indexes for this example.

Author: Fabio Pani <fabiux AT fabiopani DOT com>
License: see LICENSE
"""
from pymongo import MongoClient, DESCENDING, TEXT

if __name__ == '__main__':
    articles = MongoClient().reddit.articles
    articles.create_index('subreddit_id')
    articles.create_index('id_reddit', unique=True)
    articles.create_index([('created_utc', DESCENDING)])
    articles.create_index([('title', TEXT)])
