import pygame
import numpy as np  
from bullet import Bullet
from alien import Alien

class AlienGroup(pygame.sprite.Group):
    def __init__(self, columns, rows, devided_space, SCREENWIDTH):#11,5
        super().__init__()
        self.columns = columns
        self.rows = rows
        self.direction = 1
        self.devided_space = devided_space
        self.screenwidth = SCREENWIDTH
        self.speed =1
        
        # 2d array which keeps track of the alive aliens
        self.alivealiens = [[None] * columns for y in range(rows)] 
        self.leftAliveAlien = None
        self.rightAliveAlien = None
        self.bottomAliveAliens = self.init_bottom_aliens()
        self.alienCount= columns*rows
        self.alienDeadCount =0

    def init_bottom_aliens(self):
        bottomAliveAliens = []
        for i in range(self.columns):
                bottomAliveAliens.append([self.rows-1,i])
        return bottomAliveAliens   

    def update(self):
       # try:
        if (self.rightAliveAlien.rect.x + self.speed < self.screenwidth- self.rightAliveAlien.width) and (self.leftAliveAlien.rect.x + self.speed > 0):
            for alien in self:
                alien.rect.x += self.speed
        else:
            for alien in self:
                alien.rect.y += alien.hight
            self.speed = self.speed * -1
       # except:
       #     pass
       


    def add_internal(self, *sprites):
        super(AlienGroup, self).add_internal(*sprites)
        for s in sprites:
            self.alivealiens[s.row][s.column] = s
        self.leftAliveAlien = self.alivealiens[0][0] #[0][0]
        self.rightAliveAlien = self.alivealiens[self.rows-1][self.columns-1]#[4][10]#
        

    def remove_internal(self, *sprites):
        super(AlienGroup, self).remove_internal(*sprites)
        for s in sprites:
            self.kill(s)
        #self.update_speed()


    # check if there arent any alive aliens in this column
    def update_left_outer_aliens(self, column):
        if column <self.columns:
            c=0
            for j in range(self.rows): 
                if self.alivealiens[j][column]:
                    c+=1
            if c==0:
                self.update_left_outer_aliens(column+1)
            else:
                for j in range(self.rows): 
                    if self.alivealiens[j][column]:
                        self.leftAliveAlien = self.alivealiens[j][column]
                        break

    def update_right_outer_aliens(self, column):
        if column >=0:
            c=0
            for j in range(self.rows): 
                if self.alivealiens[j][column]:
                    c+=1
            if c==0:
                self.update_right_outer_aliens(column-1)
            else:
                for j in range(self.rows): 
                    if self.alivealiens[j][column]:
                        self.rightAliveAlien = self.alivealiens[j][column]
                        break
    

    def update_bottom_aliens(self,rows,collums):
        self.bottomAliveAliens.clear()
        for i in range(collums):
            for j in reversed(range(rows)):
                if self.alivealiens[j][i]:
                    self.bottomAliveAliens.append([j,i])
                    break
                
    #def update_right_outer_aliens(self, column):
    #    if column >=0:
    #        if not self.alivealiens[:][column]:
    #            update_right_outer_aliens(column-1)
    #        else:
    #            self.rightAliveAlien = next(iter(self.alivealiens[:][column]),None)
    
    def random_shoot(self):
        bullets=[]
        for bottomalien in self.bottomAliveAliens:
            bullet = Bullet(self.alivealiens[bottomalien[0]][bottomalien[1]].rect.x, self.alivealiens[bottomalien[0]][bottomalien[1]].rect.y, +10)
            bullets.append(bullet)
        return bullets


    def update_speed(self):
        if len(self) == 1:
            self.moveTime = 200
        elif len(self) <= 10:
            self.moveTime = 400

    def kill(self, alien):
        # sets 2d alien matrix for this specific alien to None 
        self.alivealiens[alien.row][alien.column] = None
        self.alienDeadCount +=1
        # update_outer_aliens for the right movement of the aliens
        self.update_left_outer_aliens(0)
        #a = array(self.alivealiens)
        #print(a.shape)
        #print(self.columns-1)
        self.update_right_outer_aliens(self.columns-1)
        self.update_bottom_aliens(self.rows-1,self.columns-1)


