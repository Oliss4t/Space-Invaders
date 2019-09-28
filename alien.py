import pygame

class Alien(pygame.sprite.Sprite):
    """
    This class represents an Alien. It derives from the "Sprite" class in Pygame
    """
    
    def __init__(self,screen_width,screen_hight,row, column,alien_type):
        super().__init__()
        if alien_type ==1:
            self.image = pygame.transform.scale(pygame.image.load("images\\alien1.png").convert_alpha(),(64,87))
            self.points = 10
        if alien_type ==2:
            self.image = pygame.transform.scale(pygame.image.load("images\\alien2.png").convert_alpha(),(64,87))
            self.points = 20
        if alien_type ==3:
            self.image = pygame.transform.scale(pygame.image.load("images\\alien3.png").convert_alpha(),(64,87))
            self.points = 30
        # for multiplayer 
        if alien_type ==4:
            self.image = pygame.transform.scale(pygame.image.load("images\\alien2.png").convert_alpha(),(64,87))
            self.points = 20
        if alien_type ==5:
            self.image = pygame.transform.scale(pygame.image.load("images\\alien3.png").convert_alpha(),(64,87))
            self.points = 20

        self.type = alien_type    
        self.width= self.image.get_size()[0]
        self.hight= self.image.get_size()[1]
        self.row = row
        self.column = column
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_hight = screen_hight
        self.speed = 1

    def get_hight(self):
        """
        This function returns the hight.
        :return param: integer with the alien hight
        :return type: integer
        """
        return self.hight

    def get_width(self):
        """
        This function returns the width.
        :return param: integer with the alien width
        :return type: integer
        """
        return self.width
