import pygame 
from settings import *
from debug import *

class Player(pygame.sprite.Sprite):
	def __init__(self, client, pos,groups,obstacle_sprites, server, add_key = None):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.inflate(0,-26)

		self.direction = pygame.math.Vector2()
		self.speed = 5

		self.obstacle_sprites = obstacle_sprites

		# Vilken klient spelaren tillhör
		self.client = client
		self.server = server

		#	Om funktion för att lägga till en nyckel tillkommer
		self.add_key = add_key

		# Timer som har kolla på hur länge sedan alla spelares postion uppdaterades från serverns data
		self.update_pos_timer = 0

	def input(self):
		keys = pygame.key.get_pressed()

		# Kollar så det är rätt klients input som flyttar spelaren
		if self.client == self.server.my_key:

			# Förflyttning i Y-LED
			if keys[pygame.K_UP]:
				self.direction.y = -1
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
			else:
				self.direction.y = 0

			# Förflyttning i X-LED
			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
			else:
				self.direction.x = 0

			# Kollar så att det finns någon nyckel att lägga värdena i (säkerhet)
			if len(players) > 0:
					
				players[self.client]['direction_X']	= self.direction.x
				players[self.client]['direction_Y']	= self.direction.y	

	def move(self,speed):


		# Ifall antalet frames är uppnått för uppdatering av position

		if self.update_pos_timer >= UPDATE_POS_COOLDOWN and self.client != self.server.my_key:
			# Ritar spelaren efter dictionaryns positioner varannan sekund
			# Din egna spelare är uppdaterad av dig själv, resterande av servern!

			self.hitbox.x = players[self.client]['X']
			self.collision('horizontal')
			self.hitbox.y = players[self.client]['Y']
			self.collision('vertical')

			# Nollställer timern igen
			self.update_pos_timer = 0


		# Annars förflyttning som vanligt

		else:

			# Ifall spelaren är av en annan klient så bestäms rörelsen av information skickat av servern
			if self.client != self.server.my_key and self.client != None:
				self.direction.x = players[self.client]['direction_X']
				self.direction.y = players[self.client]['direction_Y']

			#Normaliserar så att längden på direction aldrig är längre än 1 och därmed samma hastighet när man går diagonalt
			if self.direction.magnitude() != 0:
				self.direction = self.direction.normalize()
			
			# Flyttar i X-led och kollar kollision
			self.hitbox.x += self.direction.x * speed
			if len(players) > 0:
				players[self.client]['X'] = self.hitbox.x
			self.collision('horizontal')

			# Flyttar i Y-led och kollar kollision
			self.hitbox.y += self.direction.y * speed
			if len(players) > 0:
				players[self.client]['Y'] = self.hitbox.y
			self.collision('vertical')

		# Ritar bilden mitt i hitboxen
		self.rect.center = self.hitbox.center
		

	def collision(self,direction):
		if direction == 'horizontal':

			for sprite in self.obstacle_sprites:

				if sprite.hitbox.colliderect(self.hitbox):

					if self.direction.x > 0: # Förflyttar höger
						self.hitbox.right = sprite.hitbox.left

					if self.direction.x < 0: # Förflyttar vänster
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':

			for sprite in self.obstacle_sprites:

				if sprite.hitbox.colliderect(self.hitbox):

					if self.direction.y > 0: # Förflyttar ned
						self.hitbox.bottom = sprite.hitbox.top

					if self.direction.y < 0: # Förflyttar upp
						self.hitbox.top = sprite.hitbox.bottom

	def update(self):
		self.input()
		self.move(self.speed)

		#Ifall spelaren inte har en klient
		if self.client == None:

			# Och jag har en klient nyckel
			if self.server.my_key != None:

				# Uppdaterar spelarens klient till klient nyckeln
				self.client = self.server.my_key

				# Om funktionen finns (ska finnas men för säkerhetens skull) så ska den aktiveras
				if self.add_key:
					self.add_key()

		# ökar timern för postions uppdatering med 1 varje frame, vid 120 uppdateras spelarnas position
		self.update_pos_timer += 1

		



