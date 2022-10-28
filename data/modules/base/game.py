import os.path

import pygame.display

from data.modules.annoyances.annoyances import Annoyances
from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WIN_EVENT, START_EVENT, RESTART_EVENT
from data.modules.base.file import ASSET_DIR
from data.modules.game.instructions import Instructions
from data.modules.lighting.lighting import Lighting
from data.modules.scenes.game_scene import GameScene
from data.modules.base.inputs import InputManager
from data.modules.base.loader import Loader
from data.modules.scenes.start_scene import StartScene
from data.modules.scenes.win_scene import WinScene


class Game:
	def __init__(self, using_flags=True):
		self.running = True

		flags = pygame.FULLSCREEN
		self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=(flags if using_flags else 0) | pygame.SCALED, vsync=1)
		self.clock = pygame.time.Clock()

		Loader.load()

		self.game_state = "start"
		self.start_scene = StartScene()
		self.game_scene = GameScene()
		self.win_scene = WinScene()

		self.instructions = Instructions()

		self.screen_brightness = 255
		self.black_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()

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

			elif event.type == START_EVENT.type:
				self.screen_brightness = 255
				pygame.mixer.music.fadeout(1000)
				self.game_state = "trans_game"

			elif event.type == WIN_EVENT.type:
				self.screen_brightness = 255
				pygame.mixer.music.fadeout(1500)
				self.game_state = "trans_win"

			elif event.type == RESTART_EVENT.type:
				self.game_state = "trans_start"
				pygame.mixer.music.fadeout(1000)

	def update(self):
		delta = self.clock.tick() / 1000
		pygame.display.set_caption(f"{round(self.clock.get_fps())}")

		self.instructions.update(delta)

		if InputManager.keys_down[pygame.K_h]:
			self.instructions.state = "descending"
		elif InputManager.keys_up[pygame.K_h]:
			self.instructions.state = "ascending"

		if self.game_state == "start":
			self.start_scene.update()
		elif self.game_state == "trans_game":
			self.start_scene.update_text()

			self.screen_brightness -= 150 * delta
			if self.screen_brightness < 0:
				self.screen_brightness = 0
				pygame.mixer.music.stop()
				pygame.mixer.music.load(os.path.join(ASSET_DIR, "main.wav"))
				pygame.mixer.music.set_volume(0.16)
				pygame.mixer.music.play(loops=-1)
				self.game_state = "game"

		elif self.game_state == "game":
			self.game_scene.update(delta)

		elif self.game_state == "trans_win":
			self.game_scene.update(delta)

			self.screen_brightness -= 100 * delta
			if self.screen_brightness < 0:
				self.screen_brightness = 0
				self.win_scene.win_text.set_text(f"Your Time Was: {round(self.game_scene.time)} seconds")

				pygame.mixer.music.stop()
				pygame.mixer.music.load(os.path.join(ASSET_DIR, "start.wav"))
				pygame.mixer.music.set_volume(0.4)
				pygame.mixer.music.play(loops=-1)

				self.game_state = "trans_win2"
		elif self.game_state == "trans_win2":
			self.win_scene.update_text()

			self.screen_brightness += 100 * delta
			if self.screen_brightness > 255:
				self.screen_brightness = 255
				self.game_state = "win"
		elif self.game_state == "win":
			self.win_scene.update()

		elif self.game_state == "trans_start":
			self.screen_brightness -= 150 * delta
			if self.screen_brightness < 0:
				self.screen_brightness = 0

				pygame.mixer.music.stop()
				pygame.mixer.music.load(os.path.join(ASSET_DIR, "start.wav"))
				pygame.mixer.music.set_volume(0.4)
				pygame.mixer.music.play(loops=-1)

				Lighting.lights.clear()
				Annoyances.annoyances.clear()
				self.game_scene = GameScene()

				self.game_state = "trans_start2"
		elif self.game_state == "trans_start2":
			self.start_scene.update_text()

			self.screen_brightness += 150 * delta
			if self.screen_brightness > 255:
				self.screen_brightness = 255
				self.game_state = "start"

	def draw(self):
		self.window.fill((66 * 0.8, 70 * 0.8, 43 * 0.8))

		if self.game_state == "start":
			self.start_scene.draw(self.window)
		elif self.game_state == "trans_game":
			self.start_scene.draw(self.window)
			self.black_screen.fill((self.screen_brightness, self.screen_brightness, self.screen_brightness))
			self.window.blit(self.black_screen, (0, 0), special_flags=pygame.BLEND_MULT)

		elif self.game_state == "game":
			self.game_scene.draw(self.window)

		elif self.game_state == "trans_win":
			self.game_scene.draw(self.window)
			self.black_screen.fill((self.screen_brightness, self.screen_brightness, self.screen_brightness))
			self.window.blit(self.black_screen, (0, 0), special_flags=pygame.BLEND_MULT)
		elif self.game_state == "trans_win2":
			self.win_scene.draw(self.window)
			self.black_screen.fill((self.screen_brightness, self.screen_brightness, self.screen_brightness))
			self.window.blit(self.black_screen, (0, 0), special_flags=pygame.BLEND_MULT)
		elif self.game_state == "win":
			self.win_scene.draw(self.window)

		elif self.game_state == "trans_start":
			self.win_scene.draw(self.window)
			self.black_screen.fill((self.screen_brightness, self.screen_brightness, self.screen_brightness))
			self.window.blit(self.black_screen, (0, 0), special_flags=pygame.BLEND_MULT)
		elif self.game_state == "trans_start2":
			self.start_scene.draw(self.window)
			self.black_screen.fill((self.screen_brightness, self.screen_brightness, self.screen_brightness))
			self.window.blit(self.black_screen, (0, 0), special_flags=pygame.BLEND_MULT)

		self.instructions.draw(self.window)

		pygame.display.flip()
