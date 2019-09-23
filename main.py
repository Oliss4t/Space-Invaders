# Space Invaders
# Created by Tassilo Henninger

import sys
import os
import pygame
import pygameMenu
import json
from ship import Ship
from alien import Alien
from bullet import Bullet
from aliengroup import AlienGroup
from asteroid import Asteroid
from player_life import Player_Life
from textbox import TextBox
from asteroid_method import create_asteroid_ellipse

ABOUT = ['Author: @{0}'.format('Tassilo Henninger'),'Email: {0}'.format('tassilo.henninger@gmail.com'),pygameMenu.locals.TEXT_NEWLINE,'Controls:',"Move: left and right arrow key or 'a' and 'd'",'Shoot: SPACEBAR', 'Pause: ESC key']
COLOR_BLACK = ( 0, 0, 0)
COLOR_WHITE = ( 255, 255, 255)
COLOR_GREY = (140,140,140)
SCREEN_WIDTH=1200
SCREEN_HEIGHT=900
ALIEN_DEFAULT_POSITION= 50
ALIEN_DEFAULT_HIGHT= 87
ALIEN_DEFAULT_WIDTH=64
COLOR_BACKGROUND = (128, 0, 128)
DIFFICULTY = ['EASY']
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCOREFILENAME = "gamescores.json"
FILEMODE = "r+"
FILETEXT = "Player: {}; Mode: {}; Score: {}\n"



class SpaceInvaders(object):
    """
    class: representing the Space Invader game object
    """
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Space Invaders")
        pygame.mouse.set_visible(0)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('images\\background.png').convert()
        self.play_menu = None
        self.play_submenu = None
        self.about_menu = None
        self.main_menu = None
        self.pause_menu = None
        self.highscore_menu = None
        self.highscore = None
        self.music_menu = None
        self.music_game = None
        self.music_game_over = None
    
       
    # -----------------------------------------------------------------------------
    # Methods
    # -----------------------------------------------------------------------------
    


    def change_difficulty(self,value, difficulty):
        """
        This function changes the difficulty of the game.
        :param value: tuple containing the data of the selected object
        :type value: tuple
        :param difficulty: Optional parameter passed as argument to add_selector
        :type difficulty: string
        :return: None
        """
        selected, index = value
        print('Selected difficulty: "{0}" ({1}) at index {2}'.format(selected, difficulty, index))
        DIFFICULTY[0] = difficulty

    def make_aliens(self,columns,rows,alien_type_list):
        """
        This function creates aliens for the current game round.
        :param columns: integer representing the amount of alien columns to create
        :type columns: integer
        :param rows: integer representing the amount of alien rows to create
        :type rows: integer
        :param alien_type_list: list containing the type of aliens to create for each row
        :type alien_type_list: list
        :return param: sprite group containing all created alien sprites
        :return type: sprite group 
        """
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
        """
        This function creates asteroids for the entire game, no round based creation.
        :param size_of_asteroid_pice: integer representing the pixelsize of an asteroid pice
        :type size_of_asteroid_pice: integer
        :param width_of_asteroid: integer representing the width of one asteroid
        :type width_of_asteroid: integer
        :param heigt_of_asteroid: integer representing the height of one asteroid
        :type heigt_of_asteroid: integer
        :param number_of_asteroids: integer representing the amount of asteroids to create
        :type number_of_asteroids: integer
        :param color: tuple containing the color rgb value for all asteroid pice sprites to create
        :type color: tuple
        :return param: sprite group containing all created asteroid sprites
        :return type: sprite group
        """
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
        """
        This function creates the player sprite with a given level.
        :param current_x: integer representing the current x position of the current player ship sprite
        :type current_x: integer
        :param current_y: integer representing the current y position of the current player ship sprite
        :type current_y: integer
        :param lvl: integer representing the lvl of the playership to create
        :type lvl: integer
        :return param: sprite playership
        :return type: sprite
        """
        player_ship = Ship(lvl)
        if lvl ==1:
            player_ship.rect.x = SCREEN_WIDTH/2 -player_ship.get_width()/2
            player_ship.rect.y = SCREEN_HEIGHT - player_ship.get_hight()
        else:
            player_ship.rect.x = current_x
            player_ship.rect.y = current_y
        return player_ship

    def load_lifes(self,count):
        """
        This function creates the player life sprites.
        :param count: integer representing the amount of life sprites to create
        :type count: integer
        :return param: list of life sprites
        :return type: list
        """
        life_draw_width =SCREEN_WIDTH *0.95
        life_draw_hight =SCREEN_HEIGHT *0.05
        player_lifes = []
        for life in range(count):
            player_life = Player_Life(life_draw_width - 50 *life ,life_draw_hight)
            player_lifes.append(player_life)
        return player_lifes

    def update_alien_params(self,alien_init_params):
        """
        This function updates all alien params to create a more difficult alienwave next round.
        :param alien_init_params: dict representing the colums,rows and alientypelist to create next round
        :type alien_init_params: dict
        :return param: dict of alien params
        :return type: dict
        """
        if alien_init_params["columns"] <9:
            alien_init_params["columns"] +=1
        elif alien_init_params["rows"] <6:
            alien_init_params["rows"] +=1
            if alien_init_params["alien_type_list"].count(1)<2:
                alien_init_params["alien_type_list"].append(1)
            elif alien_init_params["alien_type_list"].count(2)<2:
                alien_init_params["alien_type_list"].append(2)
            else:
                alien_init_params["alien_type_list"].append(3)
            alien_init_params["alien_type_list"].sort(reverse=True)
        return alien_init_params


    def play_function(self,difficulty):
        """
        Play function to start a game. Contains the main game loop
        :param difficulty: string representing of difficulty to init the game with different difficulties
        :type difficulty: string
        :return: None
        """
        self.music_menu.stop()
        self.music_game=pygame.mixer.Sound('sounds/gamemusic.wav').play(-1)
        point_counter = 0
        round_counter = 1
        player_lvl =1
        assert isinstance(difficulty, (tuple, list))
        difficulty = difficulty[0]
        assert isinstance(difficulty, str)
        asteroid_init_params = {}
        alien_init_params = {}
        player_lives = None

        if difficulty == 'EASY':
            asteroid_init_params = {"size":10,"count":4,"width":100,"heigt":60,"color":COLOR_GREY}
            alien_init_params = {"columns":5,"rows":3,"alien_type_list":[3,2,1]}
            player_lives = 3
            lvl2_points=100
            lvl3_points=300
        elif difficulty == 'MEDIUM':
            asteroid_init_params = {"size":10,"count":3,"width":100,"heigt":60,"color":COLOR_GREY}
            alien_init_params = {"columns":6,"rows":4,"alien_type_list":[3,2,1,1]}
            player_lives = 2
            lvl2_points=150
            lvl3_points=500
        elif difficulty == 'HARD':
            asteroid_init_params = {"size":10,"count":2,"width":100,"heigt":60,"color":COLOR_GREY}
            alien_init_params = {"columns":6,"rows":5,"alien_type_list":[3,2,2,1,1]}
            player_lives = 1
            lvl2_points=175
            lvl3_points=600
        else:
            raise Exception('Unknown difficulty {0}'.format(difficulty))
        
        # init all the different sprite groups for the game.
        all_sprites_list = pygame.sprite.Group()
        all_bullets_list = pygame.sprite.Group()
        all_alien_bullets_list =pygame.sprite.Group()
        all_asteroids_list = self.make_asteroid(asteroid_init_params["size"],asteroid_init_params["width"],asteroid_init_params["heigt"],asteroid_init_params["count"],asteroid_init_params["color"])
        player_life_sprite_list = self.load_lifes(player_lives)
        all_sprites_list.add(all_asteroids_list)
        all_sprites_list.add(player_life_sprite_list)

        player_ship =self.load_player(0,0,1)
        all_sprites_list.add(player_ship) 

        #create aliens
        aliens=self.make_aliens(alien_init_params["columns"],alien_init_params["rows"],alien_init_params["alien_type_list"])

        

        # pause menu
        self.create_pause_menu()
        self.main_menu.disable()
        self.pause_menu.set_fps(FPS)
        self.pause_menu.disable()

        # -------- Main Program Loop -----------
        # while player is not death
        while len(player_life_sprite_list)>0:
            self.clock.tick(60)

            #create next alienwave if the alien group is empty
            if len(aliens) <=0:
                alien_init_params=self.update_alien_params(alien_init_params)              
                aliens = self.make_aliens(alien_init_params["columns"],alien_init_params["rows"],alien_init_params["alien_type_list"])
                round_counter +=1
        
            #upgrade playership if points are reached
            if point_counter > lvl2_points and player_ship.level ==1:
                new_player_ship=self.load_player(player_ship.rect.x,player_ship.rect.y,2)
                player_ship.kill()
                player_ship = new_player_ship
                all_sprites_list.add(player_ship) 
            if point_counter > lvl3_points and player_ship.level ==2:
                new_player_ship=self.load_player(player_ship.rect.x,player_ship.rect.y,3)
                player_ship.kill()
                player_ship = new_player_ship
                all_sprites_list.add(player_ship) 

            # --- Main event loop
            events = pygame.event.get()
            for event in events: 
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.main_menu.is_disabled() and self.pause_menu.is_disabled():
                        self.pause_menu.enable()
                                  
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_ship.move_left(SCREEN_WIDTH/100,SCREEN_WIDTH)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_ship.move_right(SCREEN_WIDTH/100,SCREEN_WIDTH)
            if keys[pygame.K_SPACE]:
                if not all_bullets_list:
                    if (player_ship.level == 1):#level 1
                        bullet = Bullet(player_ship.rect.x+52 , player_ship.rect.y+20, -10)
                        all_bullets_list.add(bullet)
                        all_sprites_list.add(bullet)
                        pygame.mixer.Sound('sounds/shoot.wav').play()
                    if (player_ship.level == 2):#level 2
                        bullet1 = Bullet(player_ship.rect.x+36 , player_ship.rect.y+5, -10)
                        bullet2 = Bullet(player_ship.rect.x+67 , player_ship.rect.y+5, -10)
                        all_bullets_list.add(bullet1,bullet2)
                        all_sprites_list.add(bullet1,bullet2)
                        pygame.mixer.Sound('sounds/shoot.wav').play()
                    if (player_ship.level == 3):#level 3
                        bullet1 = Bullet(player_ship.rect.x+8 , player_ship.rect.y+30, -10)
                        bullet2 = Bullet(player_ship.rect.x+25 , player_ship.rect.y+15, -10)
                        bullet3 = Bullet(player_ship.rect.x+79 , player_ship.rect.y+15, -10)
                        bullet4 = Bullet(player_ship.rect.x+97 , player_ship.rect.y+30, -10)
                        all_bullets_list.add(bullet1,bullet2,bullet3,bullet4)
                        all_sprites_list.add(bullet1,bullet2,bullet3,bullet4)
                        pygame.mixer.Sound('sounds/shoot.wav').play()

                # Pass events to main_menu
            self.pause_menu.mainloop(events)


            # ------ Game logic -------------------------------------------------------
            # Calls update() method on every sprite in the list 
            alien_bullet = aliens.random_shoot()
            if alien_bullet is not None:
                all_sprites_list.add(alien_bullet)
                all_alien_bullets_list.add(alien_bullet)
            all_sprites_list.update()
            aliens.update()
            
            # detect bullet sprites that collide with alien sprites, if so the sprites get killed from their group and points are added to the score
            collided_bullets_aliens = pygame.sprite.groupcollide(all_bullets_list, aliens, True, True, False)
            if collided_bullets_aliens.values():
                for killed_aliens in collided_bullets_aliens.values():
                    for killed_alien in killed_aliens:
                        point_counter+=killed_alien.points

            # detect if alien bullet/ player bullet/ or alien sprites collide with asteroid sprites, if so both collided sprites get killed from their group.
            asteroid_hit = pygame.sprite.groupcollide(all_asteroids_list, all_bullets_list, True, True)
            asteroid_hit = pygame.sprite.groupcollide(all_asteroids_list, all_alien_bullets_list, True, True)
            asteroid_hit = pygame.sprite.groupcollide(all_asteroids_list, aliens, True, False)

            # detect if alien bullets hit the player ship. if so the bullet gets killed and the player lifes get reduced by 1. Death animation gets played.
            if (pygame.sprite.spritecollideany(player_ship, all_alien_bullets_list) is not None) and player_ship.got_hit == False:                  
                player_ship.get_hit()
                pygame.mixer.Sound('sounds/shipexplosion.wav').play()
                if len(player_life_sprite_list)>=1:
                    all_sprites_list.remove(player_life_sprite_list[-1])
                    player_life_sprite_list = player_life_sprite_list[:-1]
                   
            # check if aliens are on bottom of screen. if so --> game over       
            for alien in aliens:
                if alien.rect.y >= SCREEN_HEIGHT:
                    player_life_sprite_list.clear()
                    
            # check if aliens collide with the player ship. if so --> game over      
            if pygame.sprite.spritecollideany(player_ship, aliens) is not None:
                player_life_sprite_list.clear()                                

            # --- Drawing code --------------------------------------------------------
            
            # drawing all sprites
            self.screen.blit(self.background, (0, 0))
            aliens.draw(self.screen)
            all_sprites_list.draw(self.screen)
            # draw game score
            point_counter_score = pygame.font.SysFont('Consolas', 32).render(str(point_counter), True, pygame.color.Color('White'))
            self.screen.blit(point_counter_score, (100, SCREEN_HEIGHT *0.05))
            # draw round counter
            round_counter_score = pygame.font.SysFont('Consolas', 32).render(str(round_counter), True, pygame.color.Color('White'))
            self.screen.blit(round_counter_score, (SCREEN_WIDTH/2, SCREEN_HEIGHT *0.05))

            # refresh screen.
            pygame.display.flip()

        #game over
        self.music_game.stop()
        pygame.mixer.Sound('sounds/GameOver.wav').play()
        self.music_game_over = pygame.mixer.Sound('sounds/GameOver2.wav').play(-1)
        player = self.player_name_entering(difficulty,point_counter)
        self.highscore= [player,difficulty,point_counter]
        print (self.highscore)
        self.save_player_score(player,difficulty,point_counter)
        self.pause_menu.reset(1)
        self.pause_menu.disable()
        self.music_game_over.stop()
        self.music_menu = pygame.mixer.Sound('sounds/backgroundmusic.wav').play(-1)
        self.create_highscore_menu()
        self.create_main_menu()
        self.main_menu.enable()
        self.main_menu.mainloop(events)
      
          
    def player_name_entering(self,difficulty,point_counter):
        """
        This function creates the game over screen with player name entering.
        :param difficulty: string representing the current game difficulty
        :type difficulty: string
        :param point_counter: integer representing the highscore
        :type point_counter: integer
        :return param: string with the playername input
        :return type: string
        """
        CENTERSCREENPOS1 = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2-160)
        CENTERSCREENPOS2 = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2-80)
        CENTERSCREENPOS3 = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2+0)
        CENTERSCREENPOS4 = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2+40)
        CENTERSCREENPOS5 = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2+80)
        textBox = TextBox()
        textBox.rect.center = CENTERSCREENPOS5
        font = pygame.font.SysFont('Consolas', 64)
        text_over = font.render("Game Over", True, pygame.color.Color('White'))
        text_mode = font.render("Mode: "+difficulty, True, pygame.color.Color('White'))
        text_score = font.render("Score: "+str(point_counter), True, pygame.color.Color('White'))
        text_separator = font.render("--------------------------", True, pygame.color.Color('White'))
        text_rect1 = text_over.get_rect()
        text_rect2 = text_mode.get_rect()
        text_rect3 = text_score.get_rect()
        text_rect4 = text_separator.get_rect()
        text_rect1.center = CENTERSCREENPOS1
        text_rect2.center = CENTERSCREENPOS2
        text_rect3.center = CENTERSCREENPOS3
        text_rect4.center = CENTERSCREENPOS4
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(text_over, text_rect1)
            self.screen.blit(text_mode, text_rect2)
            self.screen.blit(text_score, text_rect3)
            self.screen.blit(text_separator, text_rect4)
            self.screen.blit(textBox.image, textBox.rect)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYUP:
                    if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        textBox.shiftDown = False
                if e.type == pygame.KEYDOWN:
                    textBox.add_chr(pygame.key.name(e.key))
                    if e.key == pygame.K_SPACE:
                        textBox.text += " "
                        textBox.update()
                    if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        textBox.shiftDown = True
                    if e.key == pygame.K_BACKSPACE:
                        textBox.text = textBox.text[:-1]
                        textBox.update()
                    if e.key == pygame.K_RETURN:
                        if len(textBox.text) > 0:
                            print (textBox.text)
                            return textBox.text
                            running = False

    def main_background(self):
        """
        Function used by menus, draw on background while menu is active.
        :return: None
        """
        self.screen.blit(self.background, (0, 0))

    def read_highscore(self):
        """
        This function reads the highscore from json file.
        :return param: list with all highscore strings
        :return type: list
        """
        with open(SCOREFILENAME, "r") as jsonFile:
                data = json.load(jsonFile)
        highscore_list = []
        for d in data:
            highscore_list.append('{:^13} {:^13} {:^13}'.format("Mode: "+d,"Player: "+ data[d][0]['player'],"Score: "+ str(data[d][0]['score'])))
        return highscore_list

    def save_player_score(self,player,difficulty,point_counter):
        """
        This function saves the player score.
        :param player: string representing the game player
        :type player: string
        :param difficulty: string representing the game difficulty
        :type difficulty: string
        :param score: string representing the game highscore
        :type score: string
        :return: None
        """
        try:
            with open(SCOREFILENAME, "r") as jsonFile:
                data = json.load(jsonFile)
            if difficulty not in data:
                data[difficulty] = ([{'player':player,'score':point_counter}])
                with open(SCOREFILENAME, "w") as jsonFile:
                    json.dump(data, jsonFile)
            elif data[difficulty][0]['score'] < point_counter:
                data[difficulty][0]['score'] = point_counter
                data[difficulty][0]['player'] = player
                with open(SCOREFILENAME, "w") as jsonFile:
                    json.dump(data, jsonFile)
        except Exception as e:
            print("exceptiontext: "+str(e))

    def leave_game(self):
        """
        This function leaves the game.
        :return: None
        """
        self.music_game.stop()
        self.main()

    def reset_game(self):
        """
        This function reset the game.
        :return: None
        """
        self.music_game.stop()
        self.play_function(DIFFICULTY)

    def create_pause_menu(self):
        """
        This function creates the pause menu.
        :return: None
        """
        self.pause_menu = pygameMenu.Menu(self.screen,
                            bgfun=self.main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.font.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.3),
                            menu_width=int(WINDOW_SIZE[0] * 0.3),
                            onclose=pygameMenu.events.DISABLE_CLOSE,
                            option_shadow=False,
                            title='Pause menu',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )

        self.pause_menu.add_option('Back to Menu', self.leave_game)
    
        self.pause_menu.add_option('Reset Game',self.reset_game)

        self.pause_menu.add_option('Return to game', self.pause_menu.disable)

    def create_about_menu(self):
        """
        This function creates the about menu.
        :return: None
        """
        self.about_menu = pygameMenu.TextMenu(self.screen,
                                        bgfun=self.main_background,
                                        color_selected=COLOR_WHITE,
                                        font=pygameMenu.font.FONT_BEBAS,
                                        font_color=COLOR_BLACK,
                                        font_size_title=30,
                                        font_title=pygameMenu.font.FONT_8BIT,
                                        menu_color=MENU_BACKGROUND_COLOR,
                                        menu_color_title=COLOR_WHITE,
                                        menu_height=int(WINDOW_SIZE[1] * 0.6),
                                        menu_width=int(WINDOW_SIZE[0] * 0.6),
                                        onclose=pygameMenu.events.DISABLE_CLOSE,
                                        option_shadow=False,
                                        text_color=COLOR_BLACK,
                                        text_fontsize=20,
                                        title='About',
                                        window_height=WINDOW_SIZE[1],
                                        window_width=WINDOW_SIZE[0]
                                        )
        for m in ABOUT:
            self.about_menu.add_line(m)
        self.about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
        self.about_menu.add_option('Return to menu', pygameMenu.events.BACK)

    def create_highscore_menu(self):
        """
        This function creates the highscore menu.
        :return: None
        """
        self.highscore_menu = pygameMenu.TextMenu(self.screen,
                            bgfun=self.main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.font.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=pygameMenu.events.DISABLE_CLOSE,
                            option_shadow=False,
                            title='Highscore',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )

        HIGHSCORE_LIST = self.read_highscore()
        for line in HIGHSCORE_LIST:
            self.highscore_menu.add_line(line) 
        self.highscore_menu.add_option('Return to Menu', pygameMenu.events.BACK)

    def create_play_menu(self):
        """
        This function creates the play menu.
        :return: None
        """
        self.play_menu = pygameMenu.Menu(self.screen,
                                    bgfun=self.main_background,
                                    color_selected=COLOR_WHITE,
                                    font=pygameMenu.font.FONT_BEBAS,
                                    font_color=COLOR_BLACK,
                                    font_size=30,
                                    menu_alpha=100,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_height=int(WINDOW_SIZE[1] * 0.7),
                                    menu_width=int(WINDOW_SIZE[0] * 0.7),
                                    onclose=pygameMenu.events.DISABLE_CLOSE,
                                    option_shadow=False,
                                    title='Play menu',
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )
        self.play_submenu = pygameMenu.Menu(self.screen,
                                bgfun=self.main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.5),
                                menu_width=int(WINDOW_SIZE[0] * 0.7),
                                option_shadow=False,
                                title='Submenu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
        self.play_submenu.add_option('Back', pygameMenu.events.BACK)

        self.play_menu.add_option('Start', self.play_function, DIFFICULTY)

        self.play_menu.add_selector('Select difficulty',
                            [('1 - Easy', 'EASY'),
                                ('2 - Medium', 'MEDIUM'),
                                ('3 - Hard', 'HARD')],
                            onchange=self.change_difficulty,
                            selector_id='select_difficulty')
        self.play_menu.add_option('Return to main menu', pygameMenu.events.BACK)

    def create_main_menu(self):
        """
        This function creates the main menu.
        :return: None
        """
        self.main_menu = pygameMenu.Menu(self.screen,
                            bgfun=self.main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.font.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=pygameMenu.events.DISABLE_CLOSE,
                            option_shadow=False,
                            title='Main menu',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )

        self.main_menu.add_option('Play', self.play_menu)
        self.main_menu.add_option('About', self.about_menu)
        self.main_menu.add_option('Highscore', self.highscore_menu)
        self.main_menu.add_option('Quit', pygameMenu.events.EXIT)


    def main(self):
        """
        Main program.
        :return: None
        """
        # Create menus
        self.create_play_menu()
        self.create_about_menu()
        self.create_highscore_menu()
        self.create_main_menu()

        # Configure main menu
        self.main_menu.set_fps(FPS)
        DIFFICULTY[0]  = 'EASY'
        self.music_menu = pygame.mixer.Sound('sounds/backgroundmusic.wav').play(-1)

        # Main loop
        while True:
            # Tick
            self.clock.tick(FPS)

            # Paint background
            self.main_background()

            # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if (not self.main_menu.is_enabled()):
                self.main_menu.enable()
            self.main_menu.mainloop(events)
                      
            # Flip screen
            pygame.display.flip()


if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()