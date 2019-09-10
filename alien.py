import pygame

class Alien(pygame.sprite.Sprite):
    #This class represents an Alien. It derives from the "Sprite" class in Pygame.
    
    def __init__(self,screen_width,screen_hight,row, column,alien_type):
        super().__init__()
        # Draw the Alien
        if alien_type ==1:
            self.image = pygame.transform.scale(pygame.image.load("images\\alien1.png").convert_alpha(),(64,87))
            self.points = 10
        if alien_type ==2:
            self.image = pygame.transform.scale(pygame.image.load("images\\alien2.png").convert_alpha(),(64,87))
            self.points = 20
        if alien_type ==3:
            self.image = pygame.transform.scale(pygame.image.load("images\\alien3.png").convert_alpha(),(64,87))
            self.points = 30
        self.width= self.image.get_size()[0]
        self.hight= self.image.get_size()[1]
        self.row = row
        self.column = column
        # Fetch a rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_hight = screen_hight
        self.speed = 1

    def get_hight(self):
        return self.hight

    def get_width(self):
        return self.width

   #def update(self, *args):
   #     pygame.game.screen.blit(self.image, self.rect)
   #     if (self.rect.x + self.speed < self.screen_width- self.width) and (self.rect.x + self.speed > 0):
   #         self.rect.x += self.speed
   #     else:
   #         self.rect.y += self.hight
   #         self.speed = self.speed * -1

