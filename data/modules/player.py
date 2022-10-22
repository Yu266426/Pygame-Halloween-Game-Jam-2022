import pygame

from data.modules.constants import TILE_SIZE
from data.modules.inputs import InputManager
from data.modules.loader import Loader


class Player:
	def __init__(self, pos):
		self.image = Loader.images["player"]

		self.tile_pos = pos
		self.prev_tiled_pos = self.get_v_tile_pos
		self.pos = self.get_v_tile_pos

		self.travel_time = 0.3
		self.travel_progress = 0

		self.path = []

	def set_path(self, path):
		self.path[:] = path[:]

	@property
	def get_v_tile_pos(self):
		return pygame.Vector2(self.tile_pos[0] * TILE_SIZE + TILE_SIZE / 2, self.tile_pos[1] * TILE_SIZE + TILE_SIZE / 2)

	def update(self, delta: float):
		if InputManager.keys_down[pygame.K_w]:
			self.path.append((self.tile_pos[0], self.tile_pos[1] - 1))
		if InputManager.keys_down[pygame.K_s]:
			self.path.append((self.tile_pos[0], self.tile_pos[1] + 1))
		if InputManager.keys_down[pygame.K_a]:
			self.path.append((self.tile_pos[0] - 1, self.tile_pos[1]))
		if InputManager.keys_down[pygame.K_d]:
			self.path.append((self.tile_pos[0] + 1, self.tile_pos[1]))

		self.pos = self.prev_tiled_pos.lerp(self.get_v_tile_pos, self.travel_progress)

		self.travel_progress = min(self.travel_progress + delta / self.travel_time, 1)

		if len(self.path) > 0:
			if self.pos.distance_to(self.get_v_tile_pos) < 4:
				self.prev_tiled_pos = self.get_v_tile_pos
				self.tile_pos = self.path.pop(0)
				self.travel_progress = 0
		elif self.pos.distance_to(self.get_v_tile_pos) < 4:
			self.prev_tiled_pos = self.get_v_tile_pos
			self.travel_progress = 0

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		surface.blit(self.image, self.image.get_rect(center=self.pos).topleft - camera)
