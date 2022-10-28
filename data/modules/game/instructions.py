import pygame

from data.modules.text.text import Text


class Instructions:
	def __init__(self):
		self.bg_surface = pygame.Surface((600, 600), flags=pygame.SRCALPHA).convert_alpha()
		self.bg_surface.fill((10, 10, 10))
		self.bg_surface.set_alpha(200)

		self.surface = pygame.Surface((600, 600), flags=pygame.SRCALPHA).convert_alpha()

		self.pos = pygame.Vector2(100, -600)

		self.start_pos = pygame.Vector2(100, -600)
		self.end_pos = pygame.Vector2(100, 100)

		self.pos_percentage = 0
		self.pos = self.start_pos.copy()

		self.state = "up"

		Text((300, 45), "font.ttf", 26, "light grey", "Welcome to the Cornfield!").draw(self.surface, "c")
		Text((300, 45 * 2), "font.ttf", 26, "light grey", "Will you waste valuable time").draw(self.surface, "c")
		Text((300, 45 * 3), "font.ttf", 26, "light grey", "throwing spiders off your head,").draw(self.surface, "c")
		Text((300, 45 * 4), "font.ttf", 26, "light grey", "or will you wander BLIND").draw(self.surface, "c")
		Text((300, 45 * 5), "font.ttf", 26, "light grey", "through the maze?").draw(self.surface, "c")

		Text((300, 45 * 6 + 20), "font.ttf", 26, "gold", "Click in the direction").draw(self.surface, "c")
		Text((300, 45 * 7 + 20), "font.ttf", 26, "gold", "you want to go.").draw(self.surface, "c")

		Text((300, 45 * 8 + 20), "font.ttf", 26, "gold", "Click on spiders to").draw(self.surface, "c")
		Text((300, 45 * 9 + 20), "font.ttf", 26, "gold", "throw them off the screen!").draw(self.surface, "c")

		Text((300, 45 * 10 + 40), "font.ttf", 24, "light grey", "Press Escape to close the game").draw(self.surface, "c")

	def update(self, delta: float):
		if self.state == "descending":
			self.pos_percentage += 5 * delta
			if self.pos_percentage > 1:
				self.pos_percentage = 1
				self.state = "down"
		elif self.state == "ascending":
			self.pos_percentage -= 5 * delta
			if self.pos_percentage < 0:
				self.pos_percentage = 0
				self.state = "up"

		self.pos = self.start_pos.lerp(self.end_pos, self.pos_percentage)

	def draw(self, surface: pygame.Surface):
		surface.blit(self.bg_surface, self.pos)
		surface.blit(self.surface, self.pos)
