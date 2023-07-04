import pygame
from settings import *

class UI:
    def __init__(self, level):

        # Generell
        self.surface = pygame.display.get_surface()
        self.font = get_font(UI_FONT_SIZE)
        self.level = level

        # IP - address
        self.IP = self.level.server.host
        self.IP_surf = self.font.render(self.IP, False, 'white')
        self.IP_rect = self.IP_surf.get_rect(center=(CENTRAL_X, 100))

    def draw_IP(self):
        pygame.draw.rect(self.surface, 'red', self.IP_rect.inflate(10,10))
        pygame.draw.rect(self.surface, 'green', self.IP_rect.inflate(10,10), 3)

        self.surface.blit(self.IP_surf, self.IP_rect)


    
    def update(self):
        self.draw_IP()

