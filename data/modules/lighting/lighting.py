import pygame

from data.modules.base.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.lighting.light import Light


class Lighting:
	brightness = 0.2
	lighting_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

	lights: list[Light] = []

	@classmethod
	def add_light(cls, light_source):
		cls.lights.append(light_source)
		return light_source

	@classmethod
	def remove_light(cls, light_source):
		cls.lights.remove(light_source)

	@classmethod
	def update(cls, delta):
		for light in cls.lights:
			light.update(delta)

	@classmethod
	def draw(cls, surface: pygame.Surface, camera: pygame.Vector2):
		cls.lighting_surf.fill((255 * cls.brightness, 255 * cls.brightness, 255 * cls.brightness))

		for light in cls.lights:
			light.draw(cls.lighting_surf, camera)

		# surface.blit(cls.lighting_surf, (0, 0))
		surface.blit(cls.lighting_surf, (0, 0), special_flags=pygame.BLEND_MULT)
