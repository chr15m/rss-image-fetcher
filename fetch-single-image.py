#!/usr/bin/env python

# Fetch a single image from the directory of feeds in feed-cache

import os
import sys
import urllib
from random import choice
from xml.etree import ElementTree as ET

from BeautifulSoup import BeautifulSoup
import feedparser

try:
	os.mkdir("/tmp/rss-image-fetch")
except:
	pass

feeds = [x for x in os.listdir("feed-cache") if x.endswith(".xml")]

def image_from_rss_feed(feed_file):
	feed = feedparser.parse(os.path.join("feed-cache", feed_file))
	feed_title = feed.get("feed", {}).get("title", "")
	print "Feed:", feed_title
	images = []
	# randomly select an entry in the feed
	entry = choice(feed.entries)
	print "Post:", entry["title"]
	if hasattr(entry, "content"):
		post = entry.content.pop().value
	elif hasattr(entry, "summary_detail"):
		post = entry.summary_detail.value
	else:
		post = entry.summary
	# post = getattr(entry, "content", None) or getattr(entry, "value")
	soup = BeautifulSoup(post)
	return choice([i["src"] for i in soup.findAll("img")])

def image_from_tumblr(tree):
	print "Feed:", tree.find(".//tumblelog").attrib["title"]
	post_tags = tree.findall(".//post")
	post_tag = choice(post_tags)
	post_id = post_tag.attrib['id']
	print "Post:", post_tag.attrib["slug"]
	post_date = post_tag.attrib['date-gmt'].split(" ")[0]
	return choice([p for p in post_tag.findall(".//photo-url") if int(p.attrib['max-width']) >= 1280]).text

if feeds:
	# randomly select feed file
	feed_file = choice(feeds)
	tree = ET.fromstring(file(os.path.join("feed-cache", feed_file)).read())
	# grab random image url from feed
	url = ""
	count = 0
	while not url and count < 10:
		print "Feed type:", tree.tag
		if tree.tag == "rss" or tree.tag.endswith("feed"):
			url = image_from_rss_feed(feed_file)
		elif tree.tag == "tumblr":
			url = image_from_tumblr(tree)
		count += 1
	if url:
		# download the image
		f = open('/tmp/rss-image-fetch/tmp', 'wb')
		f.write(urllib.urlopen(url).read())
		f.close()
	else:
		print >> sys.stderr, "No URL found."

