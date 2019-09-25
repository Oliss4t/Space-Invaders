import pygame

class Bonus(pygame.sprite.Sprite):
    """
    This class represents an Bonus. It derives from the "Sprite" class in Pygame
    """
    
    def __init__(self, xpos, ypos, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images\\alienbonus.png").convert_alpha(),(45,45))
        self.points = 100
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.speed = speed

    def update(self):
        """
        This function updates the Bonus image. It gets called each game loop.
        :return: None
        """
        self.rect.x += self.speed
        if self.rect.x > 1200:
            self.kill()

    def got_hit(self):
        """
        This function gets called if the bonus gets killed
        :return: None
        """
        self.kill()
        
