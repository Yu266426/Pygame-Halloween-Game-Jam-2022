import math

import pygame

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT, RESTART_EVENT
from data.modules.base.inputs import InputManager
from data.modules.base.loader import Loader
from data.modules.text.text import Text


class WinScene:
	def __init__(self):
		self.background = Loader.images["background_nt"]

		self.win_text = Text((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.4), "font.ttf", 50, "white")

		self.info_text = Text((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.7), "font.ttf", 40, "white", "Press Space To Restart")
		self.into_text_surface = pygame.Surface(self.info_text.rendered_text[1].size, flags=pygame.SRCALPHA)
		self.into_text_surface.blit(self.info_text.rendered_text[0], (0, 0))

	def update_text(self):
		self.into_text_surface.set_alpha(int(255 / 2 + math.sin(pygame.time.get_ticks() / 400) * 255 / 2))

	def update(self):
		self.update_text()
		if InputManager.keys_down[pygame.K_SPACE]:
			pygame.event.post(RESTART_EVENT)

	def draw(self, surface: pygame.Surface):
		surface.blit(self.background, (0, 0))

		self.win_text.draw(surface, "c")

		surface.blit(self.into_text_surface, (self.info_text.pos[0] - self.info_text.rendered_text[1].width / 2, self.info_text.pos[1]))
