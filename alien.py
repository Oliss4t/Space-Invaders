import pygame

class Alien(pygame.sprite.Sprite):
    #This class represents an Alien. It derives from the "Sprite" class in Pygame.
    
    def __init__(self):
        super().__init__()
        # Draw the Alien
        self.image = pygame.image.load("images\\alien.png").convert_alpha() 
        self.width= self.image.get_size()[0]
        self.hight= self.image.get_size()[1]
        # Fetch a rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def getHight(self):
        return self.hight

    def getWidth(self):
        return self.width

    # move alien right
    def moveRight(self, pixels, screenWidth):
        if (self.rect.x + pixels) <= (screenWidth - self.width):
            self.rect.x += pixels
    
    # move alien left
    def moveLeft(self, pixels, screenWidth):
        if (self.rect.x - pixels) >= 0:
            self.rect.x -= pixels