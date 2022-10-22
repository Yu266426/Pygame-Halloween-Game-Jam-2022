import pygame.display


class Game:
	def __init__(self):
		self.running = True

		flags = pygame.SCALED | pygame.FULLSCREEN
		self.window = pygame.display.set_mode((800, 800))

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False

	def update(self):
		pass

	def draw(self):
		self.window.fill("black")
		pygame.display.flip()
