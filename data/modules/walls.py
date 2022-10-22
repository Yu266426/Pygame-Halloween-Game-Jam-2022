import pygame

from data.modules.loader import Loader


class HorizontalWall:
	def __init__(self, pos):
		self.pos = pos

		self.image = Loader.images["corn1"]
		self.rect = self.image.get_rect(midleft=pos)

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		surface.blit(self.image, self.rect.topleft - camera)


class VerticalWall:
	def __init__(self, pos):
		self.pos = pos

		self.image = pygame.transform.rotate(Loader.images["corn1"], 90)
		self.rect = self.image.get_rect(midtop=pos)

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		surface.blit(self.image, self.rect.topleft - camera)