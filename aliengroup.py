import pygame
import numpy as np  
from bullet import Bullet
from alien import Alien
import random

class AlienGroup(pygame.sprite.Group):
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
        self.bottom_alive_aliens = self.alive_aliens[self.rows-1][:]

    def update(self):
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
        super(AlienGroup, self).add_internal(*sprites)
        for sprite in sprites:
            self.alive_aliens[sprite.row][sprite.column] = sprite
        self.left_alive_alien = self.alive_aliens[0][0]
        self.right_alive_alien = self.alive_aliens[self.rows-1][self.columns-1]
        
    def remove_internal(self, *sprites):
        super(AlienGroup, self).remove_internal(*sprites)
        for sprite in sprites:
            self.kill(sprite)
        
    # check if there arent any alive aliens in this column
    def update_left_outer_aliens(self, column):
        if column < self.columns:
            for j in range(self.rows): 
                if self.alive_aliens[j][column]:
                    self.left_alive_alien = self.alive_aliens[j][column]
                    break
                else:
                    self.update_left_outer_aliens(column+1)

    def update_right_outer_aliens(self, column):
        if column >=0:
            for j in range(self.rows): 
                if self.alive_aliens[j][column]:
                    self.right_alive_alien = self.alive_aliens[j][column]
                    break
                else:
                    self.update_right_outer_aliens(column-1)
  
    def update_bottom_aliens(self,rows,collums):
        self.bottom_alive_aliens.clear()
        for i in range(collums):
            for j in reversed(range(rows)):
                if self.alive_aliens[j][i]:
                    self.bottom_alive_aliens.append(self.alive_aliens[j][i])
                    break

    # a random bottom alien shoots with the probability alien_dead_count/allAliens
    def random_shoot(self):
        if len(self.bottom_alive_aliens) > 0:
            if(random.random() < (self.alien_dead_count/self.alien_count)*self.shoot_factor):
                random_bottom_alien = random.randrange(len(self.bottom_alive_aliens))
                bullet = Bullet(self.bottom_alive_aliens[random_bottom_alien].rect.x +29 , self.bottom_alive_aliens[random_bottom_alien].rect.y +27, +10)
                return bullet

    def update_speed(self):
        if self.alien_dead_count%4==0:
            if self.speed > 0:
                self.speed +=1
            else:
                self.speed -=1

    def kill(self, alien):
        self.alive_aliens[alien.row][alien.column] = None
        self.update_bottom_aliens(self.rows,self.columns)
        self.alien_dead_count +=1
        self.update_left_outer_aliens(0)
        self.update_right_outer_aliens(self.columns-1)
        self.update_speed()


