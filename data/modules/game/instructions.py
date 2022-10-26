import pygame

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Instructions:
	def __init__(self):
		self.surface = pygame.Surface(int(SCREEN_WIDTH * 0.75), int(SCREEN_HEIGHT * 0.75))
		self.pos = pygame.Vector2(SCREEN_WIDTH * 0.125, -SCREEN_HEIGHT * 0.75)

		self.start_pos = pygame.Vector2(int(SCREEN_WIDTH * 0.125), int(-SCREEN_HEIGHT * 0.875))
		self.end_pos = pygame.Vector2(int(SCREEN_WIDTH * 0.125), int(SCREEN_HEIGHT * 0.125))
