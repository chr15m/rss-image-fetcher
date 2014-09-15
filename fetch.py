#!/usr/bin/python

import os
import sys
import urllib
from random import choice

from BeautifulSoup import BeautifulSoup
import feedparser

feeds = [x for x in os.listdir("feed-cache") if x.endswith(".xml")]

if feeds:
	# fetch a randomly selected feed
	feed_file = choice(feeds)
	feed = feedparser.parse(os.path.join("feed-cache", feed_file))
	feed_title = feed.get("feed", {}).get("title", "")
	print feed_title
	images = []
	# randomly select an entry in the feed
	entry = choice(feed.entries)
	print entry["title"]
	if hasattr(entry, "content"):
		post = entry.content.pop().value
	elif hasattr(entry, "summary_detail"):
		post = entry.summary_detail.value
	else:
		post = entry.summary
	# post = getattr(entry, "content", None) or getattr(entry, "value")
	soup = BeautifulSoup(post)
	img_url = choice([i["src"] for i in soup.findAll("img")])
	extension = img_url.split(".").pop()
	f = open('tmp.' + extension, 'wb')
	f.write(urllib.urlopen(img_url).read())
	f.close()
