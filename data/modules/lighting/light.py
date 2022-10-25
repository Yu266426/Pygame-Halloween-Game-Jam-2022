import math

import pygame


class Light:
	def __init__(self, pos, brightness, radius, variation, variation_speed, linked_pos=True, camera_affected=True):
		self.start_time = pygame.time.get_ticks() / 1000

		self.pos = pos if linked_pos else pygame.Vector2(pos)

		self.brightness = brightness
		self.radius = radius

		self.variation = variation
		self.variation_speed = variation_speed

		self.surf = pygame.Surface(((self.radius + self.variation) * 2, (self.radius + self.variation) * 2), flags=pygame.SRCALPHA).convert_alpha()

		self.camera_affected = camera_affected

	def update(self, delta):
		pass

	def draw(self, surface: pygame.Surface, camera: pygame.Vector2):
		current_time = pygame.time.get_ticks() / 1000
		variation = math.sin((current_time - self.start_time) * self.variation_speed) * self.variation

		colour = max(0, min(255, 255 * self.brightness + variation / 20))
		self.surf.fill((0, 0, 0))
		pygame.draw.circle(self.surf, (colour, colour, colour), (self.surf.get_width() / 2, self.surf.get_height() / 2), self.radius + variation)

		if self.camera_affected:
			surface.blit(self.surf, self.surf.get_rect(center=self.pos - camera), special_flags=pygame.BLEND_ADD)
		else:
			surface.blit(self.surf, self.surf.get_rect(center=self.pos), special_flags=pygame.BLEND_ADD)
