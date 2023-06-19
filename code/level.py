import pygame 
from settings import *
from server import *
from tile import Tile
from player import Player
from debug import debug

class Level():
	def __init__(self, server):

		# Hämtar servern så vi kan kalla nägra funktioner
		self.server = server

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# Tom dictionary att lägga in alla spelare med nyckel som är dess IP
		self.active_players = {}

		# sprite setup
		self.create_map()

	

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
				if col == 'p':
					if self.server.this_is_host == True:
						player = Player(self.server.my_key, (x,y),[self.visible_sprites],self.obstacle_sprites, self.server)
						self.active_players[self.server.my_key] = player
					else:
						player = Player(None, (x,y),[self.visible_sprites],self.obstacle_sprites, self.server, self.add_key)
						self.active_players[None] = player

	def add_key(self):
		# Skapar en ny dictionary så vi kan ändra nycklarna
		new_dic = {}

		for key, values in self.active_players.items():

			# Ifall nyckeln är None så ändras den till din klient IP
			if key == None:
				new_key = self.server.my_key
			else:
				new_key = key
			
			new_dic[new_key] = values
		
		# Byter ut den gamla dictionaryn till den nya
		self.active_players = new_dic
			

	def player_join(self):

		for client, _ in players.items():
			if not client in self.active_players:

				x = players[client]['X'] * TILESIZE
				y = players[client]['Y'] * TILESIZE

				player = Player(client, (x,y), [self.visible_sprites], self.obstacle_sprites, self.server)
				self.active_players[client] = player

	def run(self):
		# update and draw the game
		if self.server.my_key in self.active_players:
			self.visible_sprites.custom_draw(self.active_players[self.server.my_key])
		self.visible_sprites.update()
		self.player_join()




class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
