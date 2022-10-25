import random

import pygame

from data.modules.base.loader import Loader

grass_options = ["grass1", "grass2"]


class Grass:
	def __init__(self, pos):
		self.pos = pos

		self.image = Loader.images[random.choice(grass_options)]
		self.rect = self.image.get_rect(topleft=pos)

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		surface.blit(self.image, self.rect.topleft - camera)
