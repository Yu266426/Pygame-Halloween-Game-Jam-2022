import pygame

from data.modules.base.constants import TILE_SIZE
from data.modules.base.inputs import InputManager
from data.modules.lighting.light import Light
from data.modules.lighting.lighting import Lighting
from data.modules.base.loader import Loader


class Player:
	def __init__(self, pos):
		self.image = Loader.images["player"]

		self.tile_pos = pos
		self.prev_tiled_pos = self.get_v_tile_pos
		self.pos = pygame.Vector2()
		self.pos.xy = self.get_v_tile_pos.xy

		self.travel_time = 0.3
		self.travel_progress = 0

		self.path = []

		Lighting.add_light(Light(self.pos, 0.9, 100, 30, 2))
		Lighting.add_light(Light(self.pos, 0.5, 120, 20, 2))
		Lighting.add_light(Light(self.pos, 0.2, 150, 10, 2))

	def set_path(self, path):
		self.path[:] = path[:]

	@property
	def get_v_tile_pos(self):
		return pygame.Vector2(self.tile_pos[0] * TILE_SIZE + TILE_SIZE / 2, self.tile_pos[1] * TILE_SIZE + TILE_SIZE / 2)

	def cheaty_movement(self):
		if InputManager.keys_down[pygame.K_w]:
			self.path.append((self.tile_pos[0], self.tile_pos[1] - 1))
		if InputManager.keys_down[pygame.K_s]:
			self.path.append((self.tile_pos[0], self.tile_pos[1] + 1))
		if InputManager.keys_down[pygame.K_a]:
			self.path.append((self.tile_pos[0] - 1, self.tile_pos[1]))
		if InputManager.keys_down[pygame.K_d]:
			self.path.append((self.tile_pos[0] + 1, self.tile_pos[1]))

	def update(self, delta: float):
		# self.cheaty_movement()

		self.pos.xy = self.prev_tiled_pos.lerp(self.get_v_tile_pos, self.travel_progress).xy
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
