import pygame

class Alien(pygame.sprite.Sprite):
    #This class represents an Alien. It derives from the "Sprite" class in Pygame.
    
    def __init__(self,screenWidth,screenHight,row, column):
        super().__init__()
        # Draw the Alien
        self.image = pygame.transform.scale(pygame.image.load("images\\alien1.png").convert_alpha(),(64,87))
        self.width= self.image.get_size()[0]
        self.hight= self.image.get_size()[1]
        self.row = row
        self.column = column
        # Fetch a rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.screenWidth = screenWidth
        self.screenHight = screenHight
        self.speed = 1

    def getHight(self):
        return self.hight

    def getWidth(self):
        return self.width

   #def update(self, *args):
        #pygame.game.screen.blit(self.image, self.rect)
   #     if (self.rect.x + self.speed < self.screenWidth- self.width) and (self.rect.x + self.speed > 0):
   #         self.rect.x += self.speed
   #     else:
   #         self.rect.y += self.hight
   #         self.speed = self.speed * -1

