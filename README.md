Fetch and display random images from RSS feeds. Good for showing your Pinterest or favourite Tumblr image blogs on a Raspberry Pi driven picture frame.

# Configure #

Create a file called feeds.txt with a list of RSS/Atom image feeds in it like this:

	http://conceptships.blogspot.com/feeds/posts/default
	http://feeds.feedburner.com/FreshInspirationForYourHome

Tumblr feeds take the following form (replace TUMBLRNAME):

	http://TUMBLRNAME.tumblr.com/api/read?type=photo

Put `pull-feeds.sh` in a crontab updating about once a day or so.

Put `fetch-single-image.py` in a crontab updating every few minutes.

Then run `show-image-fullscreen.py` on your device.

# Dependencies #

To set up the required dependencies you can `pip install -r requirements.txt`. I recommend using virtualenv to keep the dependencies localised to the project rather than clobbering your system.

# License #

GPLv3 licensed, Copyright Chris McCormick, 2014.
