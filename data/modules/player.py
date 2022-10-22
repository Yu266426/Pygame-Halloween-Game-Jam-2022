import pygame 

from data.modules.constants import TILE_SIZE
from data.modules.inputs import InputManager
from data.modules.loader import Loader


class Player:
	def __init__(self, pos):
		self.tile_pos = pos
		self.pos = pygame.Vector2(pos[0] * TILE_SIZE + TILE_SIZE / 2, pos[1] * TILE_SIZE + TILE_SIZE / 2)

		self.image = Loader.images["player"]

		self.input = pygame.Vector2()

	def get_inputs(self):
		self.input.x = InputManager.keys_pressed[pygame.K_d] - InputManager.keys_pressed[pygame.K_a]
		self.input.y = InputManager.keys_pressed[pygame.K_s] - InputManager.keys_pressed[pygame.K_w]

		if self.input.length() != 0:
			self.input.normalize()

	def update(self, delta):
		self.get_inputs()

		self.pos += self.input * 5 * delta

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		surface.blit(self.image, self.image.get_rect(center=self.pos).topleft - camera)
