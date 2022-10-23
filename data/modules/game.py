import pygame.display

from data.modules.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.inputs import InputManager
from data.modules.lighting import Lighting
from data.modules.loader import Loader
from data.modules.maze import Maze, Dirs
from data.modules.player import Player
from data.modules.utils import get_tiled_pos


class Game:
	def __init__(self):
		self.running = True

		using_flags = False
		flags = pygame.FULLSCREEN
		self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=(flags if using_flags else 0) | pygame.SCALED, vsync=1)
		self.clock = pygame.time.Clock()

		Loader.load()

		self.camera = pygame.Vector2()

		self.maze = Maze((30, 30))

		self.player = Player((0, 0))

		self.path = None

	def handle_events(self):
		InputManager.reset()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False

				if event.key <= 512:
					InputManager.keys_down[event.key] = True

			elif event.type == pygame.KEYUP:
				if event.key <= 512:
					InputManager.keys_up[event.key] = True

			elif event.type == pygame.MOUSEBUTTONDOWN:
				button = event.button - 1
				if button <= 2:
					InputManager.mouse_down[button] = True

			elif event.type == pygame.MOUSEBUTTONUP:
				button = event.button - 1
				if button <= 2:
					InputManager.mouse_up[button] = True

	def update_camera(self, delta):
		self.camera = self.camera.lerp(self.player.pos - (400, 400), min(2 * delta, 1))
		if self.camera.x < -200:
			self.camera.x = -200
		if self.camera.y < -200:
			self.camera.y = -200

	def update(self):
		delta = self.clock.tick() / 1000
		pygame.display.set_caption(f"{round(self.clock.get_fps())}")

		self.maze.update()
		self.player.update(delta)

		Lighting.update(delta)

		if InputManager.mouse_down[0]:
			self.path = self.maze.find_path(self.player.tile_pos, get_tiled_pos(pygame.mouse.get_pos() + self.camera))
			if self.path is not None:
				self.player.set_path(self.path)

		self.update_camera(delta)

	# tile_mouse_pos = get_tiled_pos(pygame.mouse.get_pos() + self.camera)
	# if 0 <= tile_mouse_pos[0] < self.maze.size[0] and 0 <= tile_mouse_pos[1] < self.maze.size[1]:
	# 	tile_num = self.maze.tiles[tile_mouse_pos[1]][tile_mouse_pos[0]]
	# 	print(
	# 		tile_num,
	# 		"up:", tile_num & Dirs.UP,
	# 		"down:", tile_num & Dirs.DOWN,
	# 		"left:", tile_num & Dirs.LEFT,
	# 		"right:", tile_num & Dirs.RIGHT
	# 	)

	def draw(self):
		self.window.fill("black")

		# if self.path is not None:
		# 	for tile in self.path:
		# 		pygame.draw.rect(self.window, "blue", pygame.Rect(tile[0] * TILE_SIZE - self.camera.x, tile[1] * TILE_SIZE - self.camera.y, TILE_SIZE, TILE_SIZE))

		self.maze.draw(self.window, self.camera)
		self.player.draw(self.window, self.camera)

		Lighting.draw(self.window, self.camera)

		pygame.display.flip()
