import pygame

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,size,x,y,color):
        super().__init__()
        self.size = size
        self.color = color
        self.image = pygame.Surface( (self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))


