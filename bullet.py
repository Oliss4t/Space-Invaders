import pygame

#This class represents an Bullet. It derives from the "Sprite" class in Pygame.
class Bullet(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos, speed):
        super().__init__()
        self.image = pygame.image.load("images\\bullet.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.speed = speed

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.y < 15:
            self.kill()