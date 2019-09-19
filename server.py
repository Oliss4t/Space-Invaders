from __future__ import print_function
import sys
from time import sleep, localtime
from random import randint
from weakref import WeakKeyDictionary
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

import os
import pygame
import json
from ship import Ship
from alien import Alien
from bullet import Bullet
from aliengroup import AlienGroup
from asteroid import Asteroid
from player_life import Player_Life
from asteroid_method import create_asteroid_ellipse

SCREEN_WIDTH=1200
SCREEN_HEIGHT=900
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
ALIEN_DEFAULT_POSITION= 50
ALIEN_DEFAULT_HIGHT= 87
ALIEN_DEFAULT_WIDTH=64
COLOR_BLACK = ( 0, 0, 0)
COLOR_WHITE = ( 255, 255, 255)
COLOR_GREY = (140,140,140)

class ClientChannel(Channel):
    def Network(self, data):
        print (data)

    def Network_move(self, data):
        print ("move:", data)
        #deconsolidate all of the data from the dictionary
        #horizontal or vertical?
        #x of placed line
        x = data["x"]
        #y of placed line
        y = data["y"]
        #player number (1 or 0)
        num=data["num"]
        #id of game given by server at start of game
        self.gameid = data["gameid"]
        #tells server to place line
        self._server.placeLine( data, self.gameid, num)

    def Network_shoot(self, data):
        print ("shoot:", data)

    def Network_update(self, data):
        print ("update:", data)
    

class MyServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        
        self.games = []
        self.queue = None
        self.currentIndex=0
        print('Server launched')
        self.channelClass = ClientChannel

            
    def Connected(self, channel, addr):
        print ('new connection:', channel)
        if self.queue==None:
            self.currentIndex+=1
            channel.gameid=self.currentIndex
            self.queue=Game(channel, self.currentIndex)
        else:
            channel.gameid=self.currentIndex
            self.queue.player1=channel
            self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue=None
    
    def Launch(self):
        while True:
            self.tick()
            sleep(0.0001)
    
    def move(self, x, y, data, gameid, num):
        game = [a for a in self.games if a.gameid==gameid]
        if len(game)==1:
            game[0].move( x, y, data, num)

    def shoot(self, x, y, data, gameid, num):
        game = [a for a in self.games if a.gameid==gameid]
        if len(game)==1:
            game[0].shoot( x, y, data, num)



    def tick(self):
        
        for game in self.games:
            print("tick called")
            if len(game.aliens) <=0:
                #game.alien_init_params=self.update_alien_params(alien_init_params)              
                game.aliens = game.make_aliens(game.alien_init_params["columns"],game.alien_init_params["rows"],game.alien_init_params["alien_type_list"])

            alien_bullet = game.aliens.random_shoot()
            if alien_bullet is not None:
                game.all_sprites_list.add(alien_bullet)
                game.all_alien_bullets_list.add(alien_bullet)
            game.all_sprites_list.update()
            game.aliens.update()

            
            collided_bullets_aliens = pygame.sprite.groupcollide(game.all_bullets_list, game.aliens, True, True, False)
            if collided_bullets_aliens.values():
                for killed_aliens in collided_bullets_aliens.values():
                    for killed_alien in killed_aliens:
                        game.point_counter+=killed_alien.points

            pygame.sprite.groupcollide(game.all_asteroids_list, game.all_bullets_list, True, True)
            pygame.sprite.groupcollide(game.all_asteroids_list, game.all_alien_bullets_list, True, True)
            pygame.sprite.groupcollide(game.all_asteroids_list, game.aliens, True, False)
               

            if (pygame.sprite.spritecollideany(game.player0_ship, game.all_alien_bullets_list) is not None) and game.player0_ship.got_hit == False:                  
                game.player0_ship.get_hit()
                if len(game.player0_life_sprite_list)>=1:
                    game.all_sprites_list.remove(game.player0_life_sprite_list[-1])
                    game.player0_life_sprite_list = game.player0_life_sprite_list[:-1]
            if (pygame.sprite.spritecollideany(game.player1_ship, game.all_alien_bullets_list) is not None) and game.player1_ship.got_hit == False:                  
                game.player1_ship.get_hit()
                if len(game.player1_life_sprite_list)>=1:
                    game.all_sprites_list.remove(game.player1_life_sprite_list[-1])
                    game.player1_life_sprite_list = game.player1_life_sprite_list[:-1]
            # check if aliens are on bottom of screen        
            for alien in game.aliens:
                if alien.rect.y >= SCREEN_HEIGHT:
                    game.player0_life_sprite_list.clear()
                    game.player1_life_sprite_list.clear()
            if (pygame.sprite.spritecollideany(game.player0_ship, game.aliens) is not None) or (pygame.sprite.spritecollideany(game.player1_ship, game.aliens) is not None):
                game.player0_life_sprite_list.clear()
                game.player1_life_sprite_list.clear()  
    
       
            self.gameid=0
            game.player1.Send({"action":"update", "all_sprites_list":repr(game.all_sprites_list),"all_bullets_list":repr(game.all_bullets_list),"all_alien_bullets_list":repr(game.all_alien_bullets_list),
             "all_asteroids_list":repr(game.all_asteroids_list), "player0_life_sprite_list":repr(game.player0_life_sprite_list),"aliens":repr(game.aliens),"point_counter": game.point_counter})
            game.player0.Send({"action":"update", "all_sprites_list":repr(game.all_sprites_list),"all_bullets_list":repr(game.all_bullets_list),"all_alien_bullets_list":repr(game.all_alien_bullets_list),
             "all_asteroids_list":repr(game.all_asteroids_list), "player0_life_sprite_list":repr(game.player0_life_sprite_list),"aliens":repr(game.aliens),"point_counter": game.point_counter})
      
        self.Pump()
    
        

class Game:
    def __init__(self, player0, currentIndex):
        print("game created")
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.asteroid_init_params = {"size":10,"count":3,"width":100,"heigt":60,"color":COLOR_GREY}
        self.alien_init_params = {"columns":6,"rows":4,"alien_type_list":[3,2,1,1]}
        self.player0_lives = 2
        self.player1_lives = 2
        #initialize the players including the one who started the game
        #self.players = [player0]
        self.player0=player0
        self.player1=None
        self.playerships = [self.player0,self.player1]
        #gameid of game
        self.point_counter =0
        self.gameid=currentIndex

        self.all_sprites_list = pygame.sprite.Group()
        self.all_bullets_list = pygame.sprite.Group()
        self.all_alien_bullets_list =pygame.sprite.Group()
        self.all_asteroids_list = self.make_asteroid(self.asteroid_init_params["size"],self.asteroid_init_params["width"],self.asteroid_init_params["heigt"],self.asteroid_init_params["count"],self.asteroid_init_params["color"])
        self.player0_life_sprite_list = self.load_lifes(self.player0_lives)
        self.player1_life_sprite_list = self.load_lifes(self.player1_lives)
        self.all_sprites_list.add(self.all_asteroids_list)
        self.all_sprites_list.add(self.player0_life_sprite_list)
        self.all_sprites_list.add(self.player1_life_sprite_list)
        self.player0_ship =self.load_player(0,0,1)
        self.player1_ship =self.load_player(0,0,1)
        self.all_sprites_list.add(self.player0_ship)
        self.all_sprites_list.add(self.player1_ship) 
        self.aliens=self.make_aliens(self.alien_init_params["columns"],self.alien_init_params["rows"],self.alien_init_params["alien_type_list"])

    
    def move(self, x, y, data, num):
        #send data and turn data to each player
        self.player0.Send(data)
        self.player1.Send(data)

    def shoot(self, x, y, data, num):

        bullet = Bullet(playerships[num].rect.x+70 , playerships[num].rect.y+20, -10)
        self.all_bullets_list.add(bullet)
        self.all_sprites_list.add(bullet)
        #send data and turn data to each player
        self.player0.Send(data)
        self.player1.Send(data)

    def load_lifes(self,count):
        life_draw_width =SCREEN_WIDTH *0.95
        life_draw_hight =SCREEN_HEIGHT *0.05
        player_lifes = []
        for life in range(count):
            player_life = Player_Life(life_draw_width - 50 *life ,life_draw_hight)
            player_lifes.append(player_life)
        return player_lifes
    
    def make_aliens(self,columns,rows,alien_type_list):
        alien_type =1
        devided_space =(SCREEN_WIDTH-2*ALIEN_DEFAULT_POSITION)/columns
        aliens = AlienGroup(columns, rows, devided_space, SCREEN_WIDTH)
        for row in range(rows):
            for column in range(columns):
                alien = Alien(SCREEN_WIDTH,SCREEN_HEIGHT,row, column,alien_type_list[row])
                alien.rect.x = ALIEN_DEFAULT_POSITION + ((column) * devided_space)
                alien.rect.y = ALIEN_DEFAULT_POSITION + ((row) * ALIEN_DEFAULT_HIGHT )
                aliens.add(alien)
        aliens.init_bottom_aliens()
        return aliens

    def make_asteroid(self, size_of_asteroid_pice,width_of_asteroid,heigt_of_asteroid,number_of_asteroids,color):
        asteroid_group = pygame.sprite.Group()
        screen_space_of_all_asteroids=SCREEN_WIDTH*0.9
        screen_space_of_one_asteroid= screen_space_of_all_asteroids/number_of_asteroids
        screen_space_start = (SCREEN_WIDTH*0.1)/2
        screen_asteroid_start_offset=(screen_space_of_one_asteroid-width_of_asteroid)/2
        for i in range(number_of_asteroids):
            asteroid_group.add(create_asteroid_ellipse(size_of_asteroid_pice,screen_space_start + screen_space_of_one_asteroid*i+screen_asteroid_start_offset
                                                        , SCREEN_HEIGHT*0.7, screen_space_start + screen_space_of_one_asteroid*i+screen_asteroid_start_offset+width_of_asteroid
                                                        , SCREEN_HEIGHT*0.7+heigt_of_asteroid,color,fill = True))
        return asteroid_group
        
    def load_player(self,current_x, current_y,lvl):
        player_ship = Ship(lvl)
        if lvl ==1:
            player_ship.rect.x = SCREEN_WIDTH/2 -player_ship.get_width()/2
            player_ship.rect.y = SCREEN_HEIGHT - player_ship.get_hight()
        else:
            player_ship.rect.x = current_x
            player_ship.rect.y = current_y
        return player_ship
    

# get command line argument of server, port
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "host:port")
        print("e.g.", sys.argv[0], "localhost:31425")
    else:
        host, port = sys.argv[1].split(":")
        s = MyServer(localaddr=(host, int(port)))
        s.Launch()
