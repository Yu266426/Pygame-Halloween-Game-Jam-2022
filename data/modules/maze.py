import enum
import random

import pygame

from data.modules.constants import TILE_SIZE
from data.modules.inputs import InputManager
from data.modules.tile import Grass
from data.modules.utils import man_dist
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

		self.ground_tiles: list[list] = [[None for _ in range(self.size[0])] for __ in range(self.size[1])]
		for row in range(self.size[1]):
			for col in range(self.size[0]):
				self.ground_tiles[row][col] = (Grass((col * TILE_SIZE, row * TILE_SIZE)))

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

	def find_path(self, start_pos, end_pos):
		# It doesn't have to work great, it just has to work

		if start_pos == end_pos:
			return None

		# Find distance
		if man_dist(start_pos, end_pos) > 7:
			return None

		# * x - y
		x_y_path = []
		if start_pos[0] <= end_pos[0]:
			x_path_end = end_pos[0]
			for x in range(start_pos[0] + 1, end_pos[0] + 1):
				if self.tiles[start_pos[1]][x - 1] & Dirs.RIGHT == 0:
					x_path_end = x - 1
					break
				x_y_path.append((x, start_pos[1]))

			if start_pos[1] <= end_pos[1]:
				for y in range(start_pos[1] + 1, end_pos[1] + 1):
					if self.tiles[y - 1][x_path_end] & Dirs.DOWN == 0:
						break
					x_y_path.append((x_path_end, y))
			else:
				for y in range(start_pos[1] - 1, end_pos[1] - 1, -1):
					if self.tiles[y + 1][x_path_end] & Dirs.UP == 0:
						break
					x_y_path.append((x_path_end, y))
		else:
			x_path_end = end_pos[0]
			for x in range(start_pos[0] - 1, end_pos[0] - 1, -1):
				if self.tiles[start_pos[1]][x + 1] & Dirs.LEFT == 0:
					x_path_end = x + 1
					break
				x_y_path.append((x, start_pos[1]))

			if start_pos[1] <= end_pos[1]:
				for y in range(start_pos[1] + 1, end_pos[1] + 1):
					if self.tiles[y - 1][x_path_end] & Dirs.DOWN == 0:
						break
					x_y_path.append((x_path_end, y))

			else:
				for y in range(start_pos[1] - 1, end_pos[1] - 1, -1):
					if self.tiles[y + 1][x_path_end] & Dirs.UP == 0:
						break
					x_y_path.append((x_path_end, y))

		# * y - x
		y_x_path = []
		if start_pos[1] <= end_pos[1]:
			y_path_end = end_pos[1]
			for y in range(start_pos[1] + 1, end_pos[1] + 1):
				if self.tiles[y - 1][start_pos[0]] & Dirs.DOWN == 0:
					y_path_end = y - 1
					break
				y_x_path.append((start_pos[0], y))

			if start_pos[0] <= end_pos[0]:
				for x in range(start_pos[0] + 1, end_pos[0] + 1):
					if self.tiles[y_path_end][x - 1] & Dirs.RIGHT == 0:
						break
					y_x_path.append((x, y_path_end))
			else:
				for x in range(start_pos[0] - 1, end_pos[0] - 1, -1):
					if self.tiles[y_path_end][x + 1] & Dirs.LEFT == 0:
						break
					y_x_path.append((x, y_path_end))
		else:
			y_path_end = end_pos[1]
			for y in range(start_pos[1] - 1, end_pos[1] - 1, -1):
				if self.tiles[y + 1][start_pos[0]] & Dirs.UP == 0:
					y_path_end = y + 1
					break
				y_x_path.append((start_pos[0], y))

			if start_pos[0] <= end_pos[0]:
				for x in range(start_pos[0] + 1, end_pos[0] + 1):
					if self.tiles[y_path_end][x - 1] & Dirs.RIGHT == 0:
						break
					y_x_path.append((x, y_path_end))
			else:
				for x in range(start_pos[0] - 1, end_pos[0] - 1, -1):
					if self.tiles[y_path_end][x + 1] & Dirs.LEFT == 0:
						break
					y_x_path.append((x, y_path_end))

		x_y_dist = man_dist(x_y_path[-1], end_pos) if len(x_y_path) > 0 else 1000
		y_x_dist = man_dist(y_x_path[-1], end_pos) if len(y_x_path) > 0 else 1000

		# Return the path that gets the closest to the destination
		if x_y_dist <= y_x_dist:
			return x_y_path
		else:
			return y_x_path

	def update(self):
		if InputManager.keys_down[pygame.K_SPACE]:
			self.tiles = self._generate_maze((0, 0))
			self._generate_walls()

	def draw_outline(self, surface: pygame.Surface, camera: pygame.Vector2):
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

		pygame.draw.line(surface, "yellow", (-camera.x, -camera.y), (self.size[0] * TILE_SIZE - camera.x, -camera.y))
		pygame.draw.line(surface, "yellow", (-camera.x, self.size[1] * TILE_SIZE - camera.y), (self.size[0] * TILE_SIZE - camera.x, self.size[1] * TILE_SIZE - camera.y))
		pygame.draw.line(surface, "yellow", (-camera.x, -camera.y), (-camera.x, self.size[1] * TILE_SIZE - camera.y))
		pygame.draw.line(surface, "yellow", (self.size[0] * TILE_SIZE - camera.x, -camera.y), (self.size[0] * TILE_SIZE - camera.x, self.size[1] * TILE_SIZE - camera.y))

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		for row in self.ground_tiles:
			for tile in row:
				tile.draw(surface, camera)

		for wall in self.walls:
			wall.draw(surface, camera)
