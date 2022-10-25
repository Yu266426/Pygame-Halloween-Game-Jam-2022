import math
import random

import pygame

from data.modules.base.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.base.loader import Loader

hanging_spider_options = ["spider1"]


class HangingSpider:
	SPAWN_RANGE = [(50, 200), (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)]

	def __init__(self):
		self.final_pos = pygame.Vector2(
			random.randint(HangingSpider.SPAWN_RANGE[0][0], HangingSpider.SPAWN_RANGE[1][0]),
			random.randint(HangingSpider.SPAWN_RANGE[0][1], HangingSpider.SPAWN_RANGE[1][1])
		)
		self.initial_pos = pygame.Vector2(self.final_pos[0], -200)

		self.descending = True
		self.bounces = 0
		self.descend_accel = 200
		self.descend_vel = random.randint(250, 350)

		self.pos = self.initial_pos.copy()
		self.image = Loader.images[random.choice(hanging_spider_options)]
		self.drawn_image = self.image

		self.radius = self.image.get_height() / 2

		self.ave_num = 20
		self.throw_vels = []

		self.after_thrown_vel = pygame.Vector2()

		self.thrown = False

	# Lighting.add_light(Light(self.pos, 0.6, self.image.get_height(), 20, 1, camera_affected=False))

	def descend(self, delta):
		if self.bounces < 2:
			self.descend_vel += self.descend_accel * delta

			if self.pos.y > self.final_pos[1]:
				self.bounces += 1
				self.descend_vel *= -0.6
				self.descend_accel *= 5

				self.pos.y = self.final_pos[1]
		else:
			self.descending = False

		self.pos.y += self.descend_vel * delta + (self.descend_accel / 2) * (delta ** 2)

	def annoy(self, delta):
		self.drawn_image = pygame.transform.rotate(self.image, math.sin(pygame.time.get_ticks() / 200))

	def selected(self, mouse_pos: pygame.Vector2):
		self.drawn_image = pygame.transform.rotate(self.image, math.sin(pygame.time.get_ticks()) * 5)

		self.throw_vels.append(mouse_pos - self.pos)
		if len(self.throw_vels) > self.ave_num:
			del self.throw_vels[0]

		self.pos.xy = mouse_pos.xy

		self.descending = False

	def unselect(self):
		self.drawn_image = self.image

		for vel in self.throw_vels:
			self.after_thrown_vel += vel
		self.after_thrown_vel /= self.ave_num

		self.after_thrown_vel *= 200

		if self.after_thrown_vel.length() > 800:
			self.thrown = True
			return True
		else:
			self.throw_vels.clear()
			self.after_thrown_vel = pygame.Vector2(0, 0)
			return False

	def leave(self, delta):
		self.pos += self.after_thrown_vel * delta
		self.after_thrown_vel.y += 2000 * delta

	def update(self, delta: float):
		if self.descending:
			self.descend(delta)
		elif not self.thrown:
			self.annoy(delta)
		else:
			self.leave(delta)

	def draw(self, surface: pygame.Surface):
		if not self.thrown:
			if self.pos.y > 0:
				pygame.draw.line(surface, "white", (self.final_pos.x, 0), self.pos, width=5)
		surface.blit(self.drawn_image, self.image.get_rect(center=self.pos))
