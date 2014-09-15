#!/usr/bin/python

import sys

from BeautifulSoup import BeautifulSoup
import feedparser

if len(sys.argv) > 1:
	feedurl = feedparser.parse(sys.argv[1])
	statusupdate = feedurl.entries[0].content
	soup = BeautifulSoup(statusupdate[0]['value'])
	print([i["src"] for i in soup.findAll("img")])
else:
	print "Usage:", sys.argv[0], "http://feed-url/"
