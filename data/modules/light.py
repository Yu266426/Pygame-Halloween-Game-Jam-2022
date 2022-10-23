import math

import pygame


class Light:
	def __init__(self, pos, brightness, radius, variation, variation_speed, linked_pos=True):
		self.pos = pos if linked_pos else pygame.Vector2(pos)

		self.brightness = brightness

		self.radius = radius

		self.variation = variation
		self.variation_speed = variation_speed

		self.start_time = pygame.time.get_ticks() / 1000

	def update(self, delta):
		pass

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		current_time = pygame.time.get_ticks() / 1000
		variation = math.sin((current_time - self.start_time) * self.variation_speed) * self.variation

		colour = max(0, min(255, 255 * self.brightness + variation / 20))
		surf = pygame.Surface(((self.radius + variation) * 2, (self.radius + variation) * 2), flags=pygame.SRCALPHA)
		pygame.draw.circle(surf, (colour, colour, colour), (surf.get_width() / 2, surf.get_height() / 2), self.radius + variation)

		surface.blit(surf, surf.get_rect(center=self.pos - camera), special_flags=pygame.BLEND_ADD)
