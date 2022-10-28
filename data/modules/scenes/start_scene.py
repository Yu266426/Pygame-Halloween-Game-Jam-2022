import math
import os

import pygame

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT, START_EVENT
from data.modules.base.file import ASSET_DIR
from data.modules.base.inputs import InputManager
from data.modules.base.loader import Loader
from data.modules.text.text import Text


class StartScene:
	def __init__(self):
		self.background = Loader.images["background"]

		self.start_text = Text((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85), "font.ttf", 35, "white", "Press Space To Start")
		self.start_text_surface = pygame.Surface(self.start_text.rendered_text[1].size, flags=pygame.SRCALPHA)
		self.start_text_surface.blit(self.start_text.rendered_text[0], (0, 0))

		self.help_text = Text((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.80), "font.ttf", 31, "white", "Press H For Instructions At Any Time")
		self.help_text_surface = pygame.Surface(self.help_text.rendered_text[1].size, flags=pygame.SRCALPHA)
		self.help_text_surface.blit(self.help_text.rendered_text[0], (0, 0))

		pygame.mixer.music.load(os.path.join(ASSET_DIR, "start.wav"))
		pygame.mixer.music.set_volume(0.4)
		pygame.mixer.music.play(loops=-1)

	def update_text(self):
		self.start_text_surface.set_alpha(int(255 / 2 + math.sin(pygame.time.get_ticks() / 400) * 255 / 2))
		self.help_text_surface.set_alpha(int(255 / 2 + math.sin(pygame.time.get_ticks() / 400) * 255 / 2))

	def update(self):
		self.update_text()

		if InputManager.keys_pressed[pygame.K_SPACE]:
			pygame.event.post(START_EVENT)

	def draw(self, surface: pygame.Surface):
		surface.blit(self.background, (0, 0))
		surface.blit(self.start_text_surface, (self.start_text.pos[0] - self.start_text.rendered_text[1].width / 2, self.start_text.pos[1]))
		surface.blit(self.help_text_surface, (self.help_text.pos[0] - self.help_text.rendered_text[1].width / 2, self.help_text.pos[1]))
