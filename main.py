import sys

import pygame

from data.modules.base.game import Game

if __name__ == '__main__':
	sys.setrecursionlimit(10000)  # I'm feeling dangerous

	pygame.init()
	pygame.mixer.init()

	game = Game()
	while game.running:
		game.handle_events()
		game.update()
		game.draw()

	pygame.mixer.quit()
	pygame.quit()
