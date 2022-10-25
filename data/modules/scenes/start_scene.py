import math

import pygame

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT, START_EVENT
from data.modules.base.inputs import InputManager
from data.modules.base.loader import Loader
from data.modules.text.text import Text


class StartScene:
	def __init__(self):
		self.background = Loader.images["background"]

		self.text = Text((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85), "font.tff", 35, "white", "Press Space To Start")
		self.text_surface = pygame.Surface(self.text.rendered_text[1].size, flags=pygame.SRCALPHA)
		self.text_surface.blit(self.text.rendered_text[0], (0, 0))

	def update(self):
		self.text_surface.set_alpha(int(255 / 2 + math.sin(pygame.time.get_ticks() / 400) * 255 / 2))

		if InputManager.keys_pressed[pygame.K_SPACE]:
			pygame.event.post(START_EVENT)

	def draw(self, surface: pygame.Surface):
		surface.blit(self.background, (0, 0))
		surface.blit(self.text_surface, (self.text.pos[0] - self.text.rendered_text[1].width / 2, self.text.pos[1]))
