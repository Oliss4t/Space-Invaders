import pygame

class Ship(pygame.sprite.Sprite):
    #This class represents a ship. It derives from the "Sprite" class in Pygame.
    
    def __init__(self):
        super().__init__()
        # Draw the ship
        self.image = pygame.transform.scale(pygame.image.load("images\\shiplvl1.png").convert_alpha(), (111, 93))
     
        # level_id for the ship-"evolvement" 
        self.level = 1
        self.width= self.image.get_size()[0]
        self.hight= self.image.get_size()[1]
        # Fetch a rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def getHight(self):
        return self.hight

    def getWidth(self):
        return self.width

    # move ship right
    def moveRight(self, pixels, screenWidth):
        if (self.rect.x + pixels) <= (screenWidth - self.width):
            self.rect.x += pixels
    
    # move ship left
    def moveLeft(self, pixels, screenWidth):
        if (self.rect.x - pixels) >= 0:
            self.rect.x -= pixels
    
    # shoot bullet/s based on the current level of the ship
    def shoot(self):
        pass
