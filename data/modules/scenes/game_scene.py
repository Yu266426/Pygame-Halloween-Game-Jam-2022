import pygame

from data.modules.annoyances.annoyances import Annoyances
from data.modules.base.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WIN_EVENT
from data.modules.base.inputs import InputManager
from data.modules.base.utils import get_tiled_pos
from data.modules.game.maze import Maze
from data.modules.game.player import Player
from data.modules.lighting.light import Light
from data.modules.lighting.lighting import Lighting


class GameScene:
	def __init__(self):
		self.mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
		Lighting.add_light(Light(self.mouse_pos, 0.5, 80, 10, 1.7, camera_affected=False))
		Lighting.add_light(Light(self.mouse_pos, 0.1, 100, 12, 1.7, camera_affected=False))

		self.maze = Maze((30, 30))
		Lighting.add_light(Light((self.maze.size[0] * TILE_SIZE - TILE_SIZE / 2, self.maze.size[1] * TILE_SIZE - TILE_SIZE / 2), 0.2, TILE_SIZE * 0.7, TILE_SIZE * 0.1, 2.5, linked_pos=False))
		Lighting.add_light(Light((self.maze.size[0] * TILE_SIZE - TILE_SIZE / 2, self.maze.size[1] * TILE_SIZE - TILE_SIZE / 2), 0.9, TILE_SIZE * 0.6, TILE_SIZE * 0.03, 2.5, linked_pos=False))

		self.camera = pygame.Vector2(-20, -20)
		self.camera_max_x = self.maze.size[0] * TILE_SIZE - SCREEN_WIDTH
		self.camera_max_y = self.maze.size[1] * TILE_SIZE - SCREEN_HEIGHT

		self.player = Player((0, 0))

		self.path = None

		self.selected_annoyance = None

		self.time = 0
		self.won = False

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
		if not self.won:
			self.time += delta

		self.mouse_pos.xy = pygame.mouse.get_pos()

		self.player.update(delta)
		self.maze.update(self.player.tile_pos)

		Annoyances.update(delta)

		if InputManager.mouse_down[0]:
			self.selected_annoyance = Annoyances.hover()
			if self.selected_annoyance is None:
				self.path = self.maze.find_path(self.player.tile_pos, get_tiled_pos(self.mouse_pos + self.camera))
				if self.path is not None:
					self.player.set_path(self.path)

		if InputManager.mouse_up[0]:
			if self.selected_annoyance is not None:
				if self.selected_annoyance.unselect():
					Annoyances.switch_to_leaving(self.selected_annoyance)
				self.selected_annoyance = None

		if self.selected_annoyance is not None:
			self.selected_annoyance.selected(self.mouse_pos)

		Lighting.update(delta)
		self.update_camera(delta)

		if not self.won and self.player.tile_pos == (self.maze.size[0] - 1, self.maze.size[1] - 1):
			pygame.event.post(WIN_EVENT)
			self.won = True

	def draw(self, surface: pygame.Surface):
		self.maze.draw(surface, self.camera)
		self.player.draw(surface, self.camera)
		self.maze.foreground_draw(surface, self.camera)

		Lighting.draw(surface, self.camera)

		Annoyances.draw(surface)
