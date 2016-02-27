# Reddit Examples
This simple example shows how to analyze most recent posts (titles) at <a href="https://www.reddit.com/">Reddit.com</a> in order to find most frequent pairs of stemmed words.

The aim is to show most discussed topics and to discover potentially new ones.

## create_indexes.py
This script creates indexes for our <code>MongoDB</code> collection. Also, it creates an empty collection if it doesn't exist yet.

## scan_reddit_topics.py
Run this script once a day: it adds newest posts (relevant info only) in our collection.

Set the variable <code>topics</code> in order to choose only topics you're interested in.

## most_frequent_pairs.py
Analyze posts back to one month in time (you can set this value for <code>fromtime</code>) and find most frequent pairs of stemmed words.

For each topic, it shows a sorted list of pairs and frequency, from most to less frequent.