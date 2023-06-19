import pygame, sys
from settings import *
from server import Server
from level import Level
import os

print(os.getcwd())

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()

		self.server = Server()
		self.server.start_thread(self.server.start_listen)
		self.level = Level(self.server)
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)
		

if __name__ == '__main__':
	game = Game()
	game.run()