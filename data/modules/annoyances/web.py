import random

import pygame

from data.modules.base.loader import Loader

web_options = ["web1", "web2"]


class Web:
	def __init__(self, pos):
		self.pos = pos

		self.image = Loader.images[random.choice(web_options)]

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		surface.blit(self.image, self.pos - camera, special_flags=pygame.BLEND_ADD)
