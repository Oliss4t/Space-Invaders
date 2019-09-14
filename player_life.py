import pygame

class Player_Life(pygame.sprite.Sprite):    
    def __init__(self,screen_x,screen_y):
        super().__init__()
        self.image = pygame.image.load("images\\life.png").convert_alpha()
        self.width= self.image.get_size()[0]
        self.hight= self.image.get_size()[1]
        self.rect = self.image.get_rect(topleft=(screen_x, screen_y))

