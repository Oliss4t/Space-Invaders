import pygame

class Bullet(pygame.sprite.Sprite):
    """
    This class represents an Bullet. It derives from the "Sprite" class in Pygame
    """

    def __init__(self, xpos, ypos, speed):
        super().__init__()
        self.image = pygame.image.load("images\\bullet.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.speed = speed

    def update(self):
        """
        This function updates the bullet image. It gets called each game loop.
        :return: None
        """
        self.rect.y += self.speed
        if self.rect.y < 15 or self.rect.y > 1200:
            self.kill()