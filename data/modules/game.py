import pygame.display

from data.modules.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.game_scene import GameScene
from data.modules.inputs import InputManager
from data.modules.loader import Loader


class Game:
	def __init__(self):
		self.running = True

		using_flags = False
		flags = pygame.FULLSCREEN
		self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=(flags if using_flags else 0) | pygame.SCALED, vsync=1)
		self.clock = pygame.time.Clock()

		Loader.load()

		self.game_scene = GameScene()

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

	def update(self):
		delta = self.clock.tick() / 1000
		pygame.display.set_caption(f"{round(self.clock.get_fps())}")

		self.game_scene.update(delta)

	def draw(self):
		self.window.fill((66 * 0.8, 70 * 0.8, 43 * 0.8))

		self.game_scene.draw(self.window)

		pygame.display.flip()
