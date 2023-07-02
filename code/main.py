import pygame, sys
from settings import *
from server import Server
from level import Level
from button import Button


class Game:
	def __init__(self, screen, clock, server, host_or_join):

		self.server = server
		self.screen = screen
		self.clock = clock
		self.level = Level(self.server)

		if host_or_join == 'host':

			self.server.start_thread(self.server.start_listen)

		elif host_or_join == 'join':

			self.server.start_thread(self.server.join_server)
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				break

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)
		

class Main_menu:
	def __init__(self):
	
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('4R4M')
		self.clock = pygame.time.Clock()
		self.game = None
		self.server = Server()

		self.central = WIDTH / 2


		self.start_host_button = Button(self.central, 200, 'Host', self.get_font(75))
		self.join_game_button = Button(self.central, 400, 'Join Game', self.get_font(75))
		self.quit_button = Button(self.central, 600, 'Quit', self.get_font(75))

	def run(self):
		while True:

			menu_mouse_pos = pygame.mouse.get_pos()

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.start_host_button.check_for_input(menu_mouse_pos):
						if self.game == None:
							self.game = Game(self.screen, self.clock, self.server,'host')
						self.game.run()

					if self.join_game_button.check_for_input(menu_mouse_pos):
						if self.game == None:
							self.game = Game(self.screen, self.clock, self.server,'join')
						self.game.run()
					
					if self.quit_button.check_for_input(menu_mouse_pos):
						try:
							self.server.server.close()
							self.server.server_shutdown = True
						except:
							pass
						pygame.quit()
						sys.exit()
			
			self.screen.fill('black')

			for button in [self.start_host_button, self.join_game_button, self.quit_button]:
				button.change_color(menu_mouse_pos)
				button.update(self.screen)

			pygame.display.update()
			self.clock.tick(FPS)

	def get_font(self, size): 
		return pygame.font.Font("../graphics/font/font.ttf", size)
		    

if __name__ == '__main__':
	main = Main_menu()
	main.run()