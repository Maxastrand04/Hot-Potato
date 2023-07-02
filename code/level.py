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
		self.start_draw = start_draw

		# Tar fram display ytan 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# Tom dictionary att lägga in alla spelare med nyckel som är dess IP
		self.active_players = {}

		# skapar mappen
		self.create_map()

	

	def create_map(self):
		# Loopar genom alla rader
		for row_index,row in enumerate(WORLD_MAP):
			# Loopar genom alla kollumner
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				# Ifall en ruta har ett 'x' så ritas en sten
				if col == 'x':
					Tile((x,y),[self.visible_sprites,self.obstacle_sprites])

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

		# Kollar efter spelarna ifall det finns en som inte är utritad
		for client, _ in players.items():

			# Om en spelare inte är med som aktiv spelare
			if not client in self.active_players:

				# Tar de initiella positionerna i x och y och ser till att de aktiva x och y är samma
				x = players[client]['init_X'] * TILESIZE
				players[client]['X'] = x
				y = players[client]['init_Y'] * TILESIZE
				players[client]['Y'] = y

				#Skapar en spelare och lägger till den i aktiva spelare
				player = Player(client, (x,y), [self.visible_sprites], self.obstacle_sprites, self.server)
				self.active_players[client] = player

	# Uppdaterar och ritar spelet
	def run(self):
		
		# Ifall servern ger ok att börja rita
		if self.server.start_draw:

			# ser till att kameran följer klientens spelare
			if self.server.my_key in self.active_players:
				self.visible_sprites.custom_draw(self.active_players[self.server.my_key])

			# Uppdaterar allt som ska ritas och kollar ifall någon spelare läggs till
			self.visible_sprites.update()
			self.player_join()
			debug(players[self.server.my_key]['hot_potato'])





class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# generrell setup
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

	def custom_draw(self,player):

		# Tar fram offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
