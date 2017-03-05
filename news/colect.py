import feedparser
import sys

feed_url = sys.argv[1]

feeds = feedparser.parse(feed_url)
title = feeds['channel']['title']

for item in feeds["items"]:
	print(item["title"]+'\n')

