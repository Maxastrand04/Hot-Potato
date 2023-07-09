import pygame, sys
from settings import *
from server import Server
from level import Level
from button import Button


class Game:
	def __init__(self, main_menu, host_or_join):

		self.main_menu = main_menu
		self.level = Level(self.main_menu.server)
		self.pause_menu = Pause_menu(self.main_menu)
		self.settings = Settings_menu(self.main_menu)

		if host_or_join == 'host':

			self.main_menu.server.start_thread(self.main_menu.server.start_listen)

		elif host_or_join == 'join':
			self.main_menu.server.start_thread(self.main_menu.server.join_server)
			
	
	def run(self):
		if not self.main_menu.kill_game:
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				keys = pygame.key.get_pressed()
				if keys[pygame.K_ESCAPE]:
					pause_action = self.pause_menu.run()
					if pause_action == 'resume':
						pass
					elif pause_action == 'quit':
						break
					elif pause_action =='settings':
						self.settings.run()

				if self.main_menu.server.unable_to_join:
					self.main_menu.server.unable_to_join = False
					self.main_menu.kill_game = True
					break

				self.main_menu.screen.fill('black')
				self.level.run()
				pygame.display.update()
				self.main_menu.clock.tick(FPS)

class Main_menu:
	def __init__(self):
	
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('4R4M')
		self.clock = pygame.time.Clock()
		self.game = None
		self.kill_game = False
		self.input_text = ''
		self.server = None

		self.start_host_button = Button(CENTRAL_X, 200, 'HOST', get_font(75))
		self.join_game_button = Button(CENTRAL_X, 400, 'JOIN GAME', get_font(75))
		self.quit_button = Button(CENTRAL_X, 600, 'QUIT', get_font(75))

	def run(self):

		# Stänger ner den aktiva servern/kopplingen för att kunna starta en ny
		if self.server:
			self.server.server_shutdown = True
			self.server = None

		while True:

			menu_mouse_pos = pygame.mouse.get_pos()

			# Om spelet dödas så ska game dödas och variablen ändras till None
			if self.kill_game:
				self.game = None

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.start_host_button.check_for_input(menu_mouse_pos):
						if not self.server:
							self.server = Server(self)
						if self.game == None:
							self.game = Game(self, 'host')
						self.game.run()

					if self.join_game_button.check_for_input(menu_mouse_pos):
						self.join_screen()
						if not self.server:
							self.server = Server(self)
						if self.game == None:
							self.game = Game(self, 'join')
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
			self.clock.tick(MENU_FPS)
	
	def join_screen(self):

		outline = pygame.Rect( 0,0, 380, 40)
		outline.center = (CENTRAL_X, 200)

		loop_variable = True
		while loop_variable:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_BACKSPACE:
						# Remove the last character from the input_text
						self.input_text = self.input_text[:-1]
					elif event.key == pygame.K_RETURN:
						# Process the entered text when the Enter key is pressed
						loop_variable = False
					else:
						# Append the pressed character to the input_text
						self.input_text += event.unicode

			self.screen.fill('black')

			font = get_font(25)

			self.text = font.render(self.input_text, True, 'red')
			text_rect = self.text.get_rect(center=(CENTRAL_X, 200))


			pygame.draw.rect(self.screen, pygame.Color('grey'), outline, 2)

			self.screen.blit(self.text, text_rect)

			pygame.display.update()
			self.clock.tick(MENU_FPS)

class Pause_menu:
	def __init__(self, main_menu):

		self.screen = main_menu.screen
		self.clock = main_menu.clock

		self.continue_button = Button(CENTRAL_X, 200, 'RESUME', get_font(75))
		self.settings_button = Button(CENTRAL_X, 400, 'SETTINGS', get_font(75))
		self.quit_button = Button(CENTRAL_X, 600, 'QUIT TO MENU', get_font(75))

	def run(self):
		while True:
			menu_mouse_pos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.continue_button.check_for_input(menu_mouse_pos):
						return	'resume'
					if self.settings_button.check_for_input(menu_mouse_pos):
						return 'settings'
					if self.quit_button.check_for_input(menu_mouse_pos):
						return 'quit'
			
			self.screen.fill('black')

			for button in [self.continue_button, self.settings_button, self.quit_button]:
				button.change_color(menu_mouse_pos)
				button.update(self.screen)
			
			pygame.display.update()
			self.clock.tick(MENU_FPS)

		
		    

if __name__ == '__main__':
	main = Main_menu()
	main.run()