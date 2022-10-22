import enum
import random

import pygame

from data.modules.constants import TILE_SIZE
from data.modules.inputs import InputManager
from data.modules.utils import get_tiled_pos
from data.modules.walls import HorizontalWall, VerticalWall


class Dirs(enum.IntEnum):
	UP = 1
	DOWN = 2
	LEFT = 8
	RIGHT = 4


class Maze:
	def __init__(self, size: tuple[int, int]):
		self.size = size

		self.tiles: list[list[int]] = self._generate_maze((0, 0))
		self.walls = []
		self._generate_walls()

	def _generate_maze(self, start_pos: tuple[int, int]):
		grid: list[list[int]] = [[0 for _ in range(self.size[0])] for _ in range(self.size[1])]

		dir_x = {Dirs.UP: 0, Dirs.DOWN: 0, Dirs.LEFT: -1, Dirs.RIGHT: 1}
		dir_y = {Dirs.UP: -1, Dirs.DOWN: 1, Dirs.LEFT: 0, Dirs.RIGHT: 0}
		opposite = {Dirs.UP: Dirs.DOWN, Dirs.DOWN: Dirs.UP, Dirs.LEFT: Dirs.RIGHT, Dirs.RIGHT: Dirs.LEFT}

		def carve_from(current_x: int, current_y: int):
			# Randomize directions
			dirs = [Dirs.UP, Dirs.DOWN, Dirs.LEFT, Dirs.RIGHT]
			random.shuffle(dirs)

			for direction in dirs:
				new_x = current_x + dir_x[direction]
				new_y = current_y + dir_y[direction]

				if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[new_y]) and grid[new_y][new_x] == 0:
					grid[current_y][current_x] |= int(direction)
					grid[new_y][new_x] |= int(opposite[direction])
					carve_from(new_x, new_y)

		carve_from(start_pos[0], start_pos[1])

		return grid

	def _generate_walls(self):
		self.walls.clear()

		for col in range(self.size[0]):
			self.walls.append(HorizontalWall((col * TILE_SIZE, 0)))

		for row_num, row in enumerate(self.tiles):
			self.walls.append(VerticalWall((0, row_num * TILE_SIZE)))
			for col_num, tile in enumerate(row):
				if tile & Dirs.DOWN == 0:
					self.walls.append(HorizontalWall((col_num * TILE_SIZE, (row_num + 1) * TILE_SIZE)))

				if tile & Dirs.RIGHT != 0:
					if (tile | self.tiles[row_num][col_num + 1]) & Dirs.DOWN == 0:
						self.walls.append(HorizontalWall((col_num * TILE_SIZE, (row_num + 1) * TILE_SIZE)))
				else:
					self.walls.append(VerticalWall(((col_num + 1) * TILE_SIZE, row_num * TILE_SIZE)))

	def update(self):
		if InputManager.keys_down[pygame.K_SPACE]:
			self.tiles = self._generate_maze((0, 0))
			self._generate_walls()

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		def draw_hor(c, r):
			pygame.draw.line(surface, "white", (c * TILE_SIZE - camera.x, (r + 1) * TILE_SIZE - camera.y), ((c + 1) * TILE_SIZE - camera.x, (r + 1) * TILE_SIZE - camera.y))

		def draw_vert(c, r):
			pygame.draw.line(surface, "white", ((c + 1) * TILE_SIZE - camera.x, r * TILE_SIZE - camera.y), ((c + 1) * TILE_SIZE - camera.x, (r + 1) * TILE_SIZE - camera.y))

		pygame.draw.rect(surface, "dark red", pygame.Rect(-camera.x, -camera.y, TILE_SIZE, TILE_SIZE))

		for row_num, row in enumerate(self.tiles):
			for col_num, tile in enumerate(row):
				if tile & Dirs.DOWN == 0:
					draw_hor(col_num, row_num)

				if tile & Dirs.RIGHT != 0:
					if (tile | self.tiles[row_num][col_num + 1]) & Dirs.DOWN == 0:
						draw_hor(col_num, row_num)
				else:
					draw_vert(col_num, row_num)

		for wall in self.walls:
			wall.draw(surface, camera)

		pygame.draw.line(surface, "yellow", (-camera.x, -camera.y), (self.size[0] * TILE_SIZE - camera.x, -camera.y))
		pygame.draw.line(surface, "yellow", (-camera.x, self.size[1] * TILE_SIZE - camera.y), (self.size[0] * TILE_SIZE - camera.x, self.size[1] * TILE_SIZE - camera.y))
		pygame.draw.line(surface, "yellow", (-camera.x, -camera.y), (-camera.x, self.size[1] * TILE_SIZE - camera.y))
		pygame.draw.line(surface, "yellow", (self.size[0] * TILE_SIZE - camera.x, -camera.y), (self.size[0] * TILE_SIZE - camera.x, self.size[1] * TILE_SIZE - camera.y))
