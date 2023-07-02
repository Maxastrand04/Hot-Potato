import pygame

class Button:
    def __init__(self, x_pos, y_pos, text_input, font, image = None):
        
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font

        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        if self.image == None:

            self.image = self.text  

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


    def update(self, screen):
        self.change_color(pygame.mouse.get_pos())
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, "red")
        else:
            self.text = self.font.render(self.text_input, True, "white")