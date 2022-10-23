import pygame

from data.modules.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.inputs import InputManager
from data.modules.light import Light
from data.modules.lighting import Lighting
from data.modules.maze import Maze
from data.modules.player import Player
from data.modules.utils import get_tiled_pos


class GameScene:
	def __init__(self):
		self.mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
		Lighting.add_light(Light(self.mouse_pos, 0.5, 80, 10, 1.7, camera_affected=False))
		Lighting.add_light(Light(self.mouse_pos, 0.1, 100, 12, 1.7, camera_affected=False))

		self.maze = Maze((30, 30))

		self.camera = pygame.Vector2()
		self.camera_max_x = self.maze.size[0] * TILE_SIZE - SCREEN_WIDTH
		self.camera_max_y = self.maze.size[1] * TILE_SIZE - SCREEN_HEIGHT

		self.player = Player((0, 0))

		self.path = None

	def update_camera(self, delta):
		self.camera = self.camera.lerp(self.player.pos - (400, 400), min(2 * delta, 1))

		buffer = 20
		if self.camera.x < -buffer:
			self.camera.x = -buffer
		if self.camera.x > self.camera_max_x + buffer:
			self.camera.x = self.camera_max_x + buffer

		if self.camera.y < -buffer:
			self.camera.y = -buffer
		if self.camera.y > self.camera_max_y + buffer:
			self.camera.y = self.camera_max_y + buffer

	def update(self, delta):
		self.mouse_pos.xy = pygame.mouse.get_pos()

		self.player.update(delta)

		Lighting.update(delta)

		if InputManager.mouse_down[0]:
			self.path = self.maze.find_path(self.player.tile_pos, get_tiled_pos(pygame.mouse.get_pos() + self.camera))
			if self.path is not None:
				self.player.set_path(self.path)

		self.update_camera(delta)

	def draw(self, surface: pygame.Surface):
		# if self.path is not None:
		# 	for tile in self.path:
		# 		pygame.draw.rect(self.window, "blue", pygame.Rect(tile[0] * TILE_SIZE - self.camera.x, tile[1] * TILE_SIZE - self.camera.y, TILE_SIZE, TILE_SIZE))

		self.maze.draw(surface, self.camera)
		self.player.draw(surface, self.camera)

		Lighting.draw(surface, self.camera)
