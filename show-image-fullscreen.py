#!/usr/bin/env python

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0))
pygame.display.toggle_fullscreen()
pygame.mouse.set_visible(False)
screensize = (screen.get_width(), screen.get_height())

path = "/tmp/rss-image-fetch"

clock = pygame.time.Clock()
done = False
reslurp = True

class ImageReloader(FileSystemEventHandler):
	def __init__(self, *args, **kwargs):
		self.rate = 4
		self.surface = pygame.Surface((1, 1))
		self.size = (0, 0)
		self.fade = False
		self.screensize = kwargs.pop("screensize")
		FileSystemEventHandler.__init__(self, *args, **kwargs)
	
	def on_any_event(self, event):
		print event.event_type, event.src_path
		if event.src_path.endswith("/tmp"):
			self.refresh()
	
	def get_surface(self):
		if self.fade:
			if self.surface.get_alpha():
				self.surface.set_alpha((self.surface.get_alpha() or 0) - self.rate)
			else:
				self.fade = False
				self.surface = self.new_surface
				self.size = self.new_size
				self.surface.set_alpha(0)
		elif int(self.surface.get_alpha() or 0) < 255:
			self.surface.set_alpha((self.surface.get_alpha() or 0) + self.rate)
		return self.surface 
	
	def refresh(self):
		try:
			picture = pygame.image.load(path + "/tmp")
		except pygame.error:
			print "Image not ready."
		else:
			print "Image refreshed."
			size = (picture.get_width(), picture.get_height())
			scale = max(float(size[1]) / self.screensize[1], float(size[0]) / self.screensize[0]);
			self.new_size = (int(size[0] / scale), int(size[1] / scale))
			self.new_surface = pygame.transform.smoothscale(picture, self.new_size)
			self.fade = True
	
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
			screen.blit(imageloader.get_surface(), imageloader.shift())
			clock.tick(60)
			pygame.display.flip()
	except KeyboardInterrupt:
		done = True
	
	pygame.quit()
	observer.stop()
	observer.join()

