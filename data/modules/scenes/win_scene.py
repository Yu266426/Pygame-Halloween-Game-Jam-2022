import pygame

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.loader import Loader
from data.modules.text.text import Text


class WinScene:
	def __init__(self):
		self.background = Loader.images["background_nt"]

		self.text = Text((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.4), "font.ttf", 50, "white")

	def update(self):
		pass

	def draw(self, surface: pygame.Surface):
		surface.blit(self.background, (0, 0))

		self.text.draw(surface, "c")
