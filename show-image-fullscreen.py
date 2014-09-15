#!/usr/bin/python

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0))
# pygame.display.toggle_fullscreen()
screensize = (screen.get_width(), screen.get_height())

path = "/tmp/rss-image-fetch"

clock = pygame.time.Clock()
done = False
reslurp = True

class ImageReloader(FileSystemEventHandler):
	def __init__(self, *args, **kwargs):
		self.surface = None
		self.size = (0, 0)
		self.screensize = kwargs.pop("screensize")
		FileSystemEventHandler.__init__(self, *args, **kwargs)
	
	def on_any_event(self, event):
		print event.event_type, event.src_path
		if event.src_path.endswith("/tmp"):
			self.refresh()
	
	def refresh(self):
		try:
			picture = pygame.image.load(path + "/tmp")
		except pygame.error:
			print "Image not ready."
		else:
			print "Image refreshed."
			size = (picture.get_width(), picture.get_height())
			scale = max(float(size[1]) / self.screensize[1], float(size[0]) / self.screensize[0]);
			self.size = (int(size[0] / scale), int(size[1] / scale))
			self.surface = pygame.transform.smoothscale(picture, self.size)
	
	def shift(self):
		return ((self.screensize[0] - self.size[0]) / 2, (self.screensize[1] - self.size[1]) / 2)

if __name__ == "__main__":
	imageloader = ImageReloader(screensize=screensize)
	imageloader.refresh()
	
	observer = Observer()
	observer.schedule(imageloader, path='/tmp/rss-image-fetch', recursive=False)
	observer.start()
	
	try:
		while not done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					done = True
			screen.fill((0, 0, 0))
			if imageloader.surface:
				screen.blit(imageloader.surface, imageloader.shift())
			clock.tick(60)
			pygame.display.flip()
	except KeyboardInterrupt:
		done = True
	
	pygame.quit()
	observer.stop()
	observer.join()

