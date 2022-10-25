import pygame

from data.modules.base.constants import SCREEN_HEIGHT


class Annoyances:
	annoyances = []
	leaving = []

	@classmethod
	def add_annoyance(cls, annoyance):
		cls.annoyances.append(annoyance)

	@classmethod
	def switch_to_leaving(cls, annoyance):
		cls.annoyances.remove(annoyance)
		cls.leaving.append(annoyance)

	@classmethod
	def hover(cls):
		mouse_pos = pygame.mouse.get_pos()
		for annoyance in cls.annoyances:
			if annoyance.pos.distance_to(mouse_pos) < annoyance.radius:
				return annoyance
		return None

	@classmethod
	def update(cls, delta: float):
		for annoyance in cls.annoyances:
			annoyance.update(delta)

		for annoyance in cls.leaving:
			annoyance.update(delta)

		for annoyance in cls.leaving:
			if annoyance.pos.y > SCREEN_HEIGHT + 200:
				cls.leaving.remove(annoyance)

	@classmethod
	def draw(cls, surface: pygame.Surface):
		for annoyance in cls.annoyances:
			annoyance.draw(surface)

		for annoyance in cls.leaving:
			annoyance.draw(surface)
