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

def image_from_apod_feed(feed_file):
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
	links = soup.findAll("a")
	apod_page = urllib.urlopen(links.pop(0)["href"])
	apod_soup = BeautifulSoup(apod_page)
	links = apod_soup.find("center").findAll("a")
	filter_image_links = [l["href"] for l in links if l["href"].endswith("jpg")]
	image = filter_image_links.pop()
	image = ("http://apod.nasa.gov/apod/" if not image.startswith("http") else "") + image
	return image

if feeds:
	# randomly select feed file
	feed_file = choice(feeds)
	tree = ET.fromstring(file(os.path.join("feed-cache", feed_file)).read())
	base_url = "/".join(file(os.path.join("feed-cache", feed_file.replace(".xml", ".url"))).readline().split("/")[:-1]) + "/"
	# grab random image url from feed
	url = ""
	count = 0
	while not url and count < 10:
		print "Feed type:", tree.tag
		if tree.find(".//title") is not None and tree.find(".//title").text == "APOD":
			url = image_from_apod_feed(feed_file) 
		elif tree.tag == "rss" or tree.tag.endswith("feed"):
			url = image_from_rss_feed(feed_file)
		elif tree.tag == "tumblr":
			url = image_from_tumblr(tree)
		count += 1
	if url:
		# download the image
		f = open('/tmp/rss-image-fetch/tmp', 'wb')
		f.write(urllib.urlopen(url.startswith("http") and url or base_url + url).read())
		f.close()
	else:
		print >> sys.stderr, "No URL found."

