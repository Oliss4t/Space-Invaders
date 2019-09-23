import pygame
import numpy as np  
from bullet import Bullet
from alien import Alien
import random

class AlienGroup(pygame.sprite.Group):
    """
    This class represents an Aliengroup. It derives from the "Sprite.Group" class in Pygame
    """
    def __init__(self, columns, rows, devided_space, SCREEN_WIDTH):
        super().__init__()
        self.columns = columns
        self.rows = rows
        self.direction = 1
        self.devided_space = devided_space
        self.screen_width = SCREEN_WIDTH
        self.speed =1
        self.timer =0
        self.timer_modulo = 2
        self.shoot_factor = 0.06
        self.alive_aliens = [[None] * columns for y in range(rows)] 
        self.left_alive_alien = None
        self.right_alive_alien = None
        self.bottom_alive_aliens = []
        self.alien_count= columns*rows
        self.alien_dead_count = 1
        
    def init_bottom_aliens(self):
        """
        This function initializes the botton aliens. 
        :return: None
        """
        self.bottom_alive_aliens = self.alive_aliens[self.rows-1][:]

    def update(self):
        """
        This function moves all aliens in the aliengroup. The movement direction changes when the right or left outer alien hits the edge of the screen. It gets called each game loop.
        :return: None
        """
        self.timer +=1
        if (self.timer%self.timer_modulo ==0):
            if (self.right_alive_alien.rect.x + self.speed < self.screen_width- self.right_alive_alien.width) and (self.left_alive_alien.rect.x + self.speed > 0):
                for alien in self:
                    alien.rect.x += self.speed
            else:
                for alien in self:
                    alien.rect.y += alien.hight
                self.speed = self.speed * -1      

    def add_internal(self, *sprites):
        """
        This function adds an alien sprite to the aliengroup.
        :param *sprites: *sprites representing alien/s
        :type *sprites: *sprites
        :return: None
        """
        super(AlienGroup, self).add_internal(*sprites)
        for sprite in sprites:
            self.alive_aliens[sprite.row][sprite.column] = sprite
        self.left_alive_alien = self.alive_aliens[0][0]
        self.right_alive_alien = self.alive_aliens[self.rows-1][self.columns-1]
        
    def remove_internal(self, *sprites):
        """
        This function removes an alien sprite from the aliengroup.
        :param *sprites: *sprites representing alien/s
        :type *sprites: *sprites
        :return: None
        """
        super(AlienGroup, self).remove_internal(*sprites)
        for sprite in sprites:
            self.kill(sprite)
        
    # check if there arent any alive aliens in this column
    def update_left_outer_aliens(self, column):
        """
        This function updates the left outer alien column. It gets called after an alien got killed.
        :param column: integer representing the column to check for alive aliens
        :type column: integer
        :return: None
        """
        if column < self.columns:
            for j in range(self.rows): 
                if self.alive_aliens[j][column]:
                    self.left_alive_alien = self.alive_aliens[j][column]
                    break
                else:
                    self.update_left_outer_aliens(column+1)

    def update_right_outer_aliens(self, column):
        """
        This function updates the right outer alien column. It gets called after an alien got killed.
        :param column: integer representing the column to check for alive aliens
        :type column: integer
        :return: None
        """
        if column >=0:
            for j in range(self.rows): 
                if self.alive_aliens[j][column]:
                    self.right_alive_alien = self.alive_aliens[j][column]
                    break
                else:
                    self.update_right_outer_aliens(column-1)
  
    def update_bottom_aliens(self,rows,columns):
        """
        This function updates the bottom alien for each column. It gets called after an alien got killed.
        :param rows: integer representing the rows of the aliengroup
        :type rows: integer
        :param columns: integer representing the columns of the aliengroup
        :type columns: integer
        :return: None
        """
        self.bottom_alive_aliens.clear()
        for i in range(columns):
            for j in reversed(range(rows)):
                if self.alive_aliens[j][i]:
                    self.bottom_alive_aliens.append(self.alive_aliens[j][i])
                    break

    def random_shoot(self):
        """
        This function makes a random bottom alien shoot with the probability alien_dead_count/allAliens. It gets called each game loop.
        :return param: bullet sprite
        :return type: sprite
        """
        if len(self.bottom_alive_aliens) > 0:
            if(random.random() < (self.alien_dead_count/self.alien_count)*self.shoot_factor):
                random_bottom_alien = random.randrange(len(self.bottom_alive_aliens))
                bullet = Bullet(self.bottom_alive_aliens[random_bottom_alien].rect.x +29 , self.bottom_alive_aliens[random_bottom_alien].rect.y +27, +10)
                pygame.mixer.Sound('sounds/shoot_alien.wav').play()
                return bullet

    def update_speed(self):
        """
        This function updates the speed of all aliens after 4 kills. It gets called after an alien got killed.
        :return: None
        """
        if self.alien_dead_count%4==0:
            if self.speed > 0:
                self.speed +=1
            else:
                self.speed -=1

    def kill(self, alien):
        """
        This function gets called if an alien gets removed from the aliengroup. It kills the alien sprite and calls left/right/bottom update functions.
        :param alien: sprite representing an alien
        :type alien: sprite
        :return: None
        """
        pygame.mixer.Sound('sounds/invaderkilled.wav').play()
        self.alive_aliens[alien.row][alien.column] = None
        self.update_bottom_aliens(self.rows,self.columns)
        self.alien_dead_count +=1
        self.update_left_outer_aliens(0)
        self.update_right_outer_aliens(self.columns-1)
        self.update_speed()



