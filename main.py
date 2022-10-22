from data.modules.game import Game

if __name__ == '__main__':
	game = Game()
	while game.running:
		game.handle_events()
		game.update()
		game.draw()
