# Space Invaders
# Created by Tassilo Henninger
import sys
import os
import pygame
import pygameMenu
from ship import Ship
from alien import Alien
from bullet import Bullet
from aliengroup import AlienGroup
from asteroid import Asteroid
from player_life import Player_Life
from text import Text
from asteroid_method import create_asteroid_ellipse, create_asteroid_ellipse2, create_asteroid_ellipse3

ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),'Author: @{0}'.format('Tassilo Henninger'),pygameMenu.locals.TEXT_NEWLINE,'Email: {0}'.format('tassilo.henninger@gmail.com')]
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



shiftDown = False
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
class TextBox(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.text = ""
            self.font = pygame.font.SysFont('Consolas', 64)
            self.image = self.font.render("Enter your name", True, pygame.color.Color('White'))
            self.rect = self.image.get_rect()

        def add_chr(self, char):
            global shiftDown
            if char in validChars and not shiftDown:
                self.text += char
            elif char in validChars and shiftDown:
                self.text += shiftChars[validChars.index(char)]
            self.update()

        def update(self):
            old_rect_pos = self.rect.center
            self.image = self.font.render(self.text,True, pygame.color.Color('White'))
            self.rect = self.image.get_rect()
            self.rect.center = old_rect_pos

class SpaceInvaders(object):
    def __init__(self):
        #global main_menu
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Space Invaders")
        pygame.mouse.set_visible(0)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('images\\background.png').convert()
        # Create pygame screen and objects
        self.play_menu = None
        self.play_submenu = None
        self.about_menu = None
        self.main_menu = None
        self.pause_menu = None
        self.highscore = None
    
    # -----------------------------------------------------------------------------
    # Constants and global variables
    # -----------------------------------------------------------------------------
        
    # -----------------------------------------------------------------------------
    # Methods
    # -----------------------------------------------------------------------------
    def change_difficulty(self,value, difficulty):
        selected, index = value
        print('Selected difficulty: "{0}" ({1}) at index {2}'.format(selected, difficulty, index))
        DIFFICULTY[0] = difficulty


    #def createAliens(numbersofrows, numberofaliensinrow):
    #    for i in range(numbersofrows):
    #        for ii in range(numberofaliensinrow):
    #            alien = Alien(SCREEN_WIDTH,SCREEN_HEIGHT)
    #            alien.rect.x = 50 + ii* 100
    #            alien.rect.y = 50 + i* 90
    #            all_sprites_list.add(alien) 
    #            all_aliens_list.add(alien)


    #make_aliens(11,5)
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
    #    self.enemies = enemies

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
        
    def make_enemies_shoot(self):
        if (time.get_ticks() - self.timer) > 700 and self.enemies:
            enemy = self.enemies.random_bottom()
            self.enemyBullets.add(
                Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5,
                        'enemylaser', 'center'))
            self.allSprites.add(self.enemyBullets)
            self.timer = time.get_ticks()

    def load_player(self,current_x, current_y,lvl):
        player_ship = Ship(lvl)
        if lvl ==1:
            player_ship.rect.x = SCREEN_WIDTH/2 -player_ship.get_width()/2
            player_ship.rect.y = SCREEN_HEIGHT - player_ship.get_hight()
        else:
            player_ship.rect.x = current_x
            player_ship.rect.y = current_y
        return player_ship

    def load_lifes(self,count):
        life_draw_width =SCREEN_WIDTH *0.95
        life_draw_hight =SCREEN_HEIGHT *0.05
        player_lifes = []
        for life in range(count):
            player_life = Player_Life(life_draw_width - 50 *life ,life_draw_hight)
            player_lifes.append(player_life)
        return player_lifes

    def play_function(self,difficulty, font, test=False):

        point_counter = 0
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
        elif difficulty == 'MEDIUM':
            asteroid_init_params = {"size":10,"count":3,"width":100,"heigt":60,"color":COLOR_GREY}
            alien_init_params = {"columns":6,"rows":4,"alien_type_list":[3,2,1,1]}
            player_lives = 2
        elif difficulty == 'HARD':
            asteroid_init_params = {"size":10,"count":2,"width":100,"heigt":60,"color":COLOR_GREY}
            alien_init_params = {"columns":8,"rows":5,"alien_type_list":[3,2,2,1,1]}
            player_lives = 1
        else:
            raise Exception('Unknown difficulty {0}'.format(difficulty))
        
        # list contains all the sprites in the game.
        all_sprites_list = pygame.sprite.Group()
        # list contains all the bullets in the game.
        all_bullets_list = pygame.sprite.Group()

        all_alien_bullets_list =pygame.sprite.Group()
      

        #asteroid = Asteroid(50,50,50,COLOR_WHITE)
        #all_sprites_list.add(asteroid)
        #size_of_asteroid_pice,width_of_asteroid,heigt_of_asteroid,number_of_asteroids
        
        all_asteroids_list = self.make_asteroid(asteroid_init_params["size"],asteroid_init_params["width"],asteroid_init_params["heigt"],asteroid_init_params["count"],asteroid_init_params["color"])
    
        player_life_sprite_list = self.load_lifes(player_lives)

        #all_asteroids_list = pygame.sprite.Group()
        #asteroids= create_asteroid_ellipse3(1,100,600,300,700,COLOR_WHITE,False)
        #all_asteroids_lisst.add(asteroids)

        all_sprites_list.add(all_asteroids_list)
        all_sprites_list.add(player_life_sprite_list)

        # creat and add the player to the list of objects
        player_ship =self.load_player(0,0,1)
        all_sprites_list.add(player_ship) 

        #create aliens
        aliens=self.make_aliens(alien_init_params["columns"],alien_init_params["rows"],alien_init_params["alien_type_list"])

        

        # pause menu
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

        self.pause_menu.add_option('Back to Menu', self.main)
    
        self.pause_menu.add_option('Reset Game',  # When pressing return -> play(DIFFICULTY[0], font)
                            self.play_function,
                            DIFFICULTY,
                            pygame.font.Font(pygameMenu.font.FONT_FRANCHISE, 30))

        self.pause_menu.add_option('Return to game', self.pause_menu.disable)
    
        # Reset main menu and disable
        # You also can set another menu, like a 'pause menu', or just use the same
        # main_menu as the menu that will check all your input.
        self.main_menu.disable()
        #pause_menu.disable()
        self.main_menu.reset(1)
        #pause_menu.reset(1)
        self.pause_menu.set_fps(FPS)
        self.pause_menu.disable()

        pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))
        RUNNING, PAUSE, EXIT = 0, 1, 2
        state = RUNNING
        # -------- Main Program Loop -----------
        while len(player_life_sprite_list)>0:
            

            # Clock tick 60 fps
            self.clock.tick(60)

            if point_counter > 100 and player_ship.level ==1:
                new_player_ship=self.load_player(player_ship.rect.x,player_ship.rect.y,2)
                player_ship.kill()
                player_ship = new_player_ship
                all_sprites_list.add(player_ship) 
            if point_counter > 200 and player_ship.level ==2:
                new_player_ship=self.load_player(player_ship.rect.x,player_ship.rect.y,3)
                player_ship.kill()
                player_ship = new_player_ship
                all_sprites_list.add(player_ship) 

            # --- Main event loop
            events = pygame.event.get()
            for event in events: # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.main_menu.is_disabled() and self.pause_menu.is_disabled():
                        self.pause_menu.enable()
                        
                    if event.key == pygame.K_p: state = PAUSE
                    if event.key == pygame.K_s: state = RUNNING
            if state == RUNNING:            
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    player_ship.move_left(SCREEN_WIDTH/100,SCREEN_WIDTH)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    player_ship.move_right(SCREEN_WIDTH/100,SCREEN_WIDTH)
                if keys[pygame.K_SPACE]:
                    if not all_bullets_list:
                        if (player_ship.level == 1):#level 1
                            bullet = Bullet(player_ship.rect.x+70 , player_ship.rect.y+20, -10)
                            all_bullets_list.add(bullet)
                            all_sprites_list.add(bullet)
                            pygame.mixer.Sound('sounds/shoot.wav').play()
                        if (player_ship.level == 2):#level 2
                            bullet1 = Bullet(player_ship.rect.x+49 , player_ship.rect.y+5, -10)
                            bullet2 = Bullet(player_ship.rect.x+83 , player_ship.rect.y+5, -10)
                            all_bullets_list.add(bullet1,bullet2)
                            all_sprites_list.add(bullet1,bullet2)
                            pygame.mixer.Sound('sounds/shoot.wav').play()
                        if (player_ship.level == 3):#level 3
                            bullet1 = Bullet(player_ship.rect.x+49 , player_ship.rect.y+5, -10)
                            bullet2 = Bullet(player_ship.rect.x+83 , player_ship.rect.y+5, -10)
                            bullet3 = Bullet(player_ship.rect.x+39 , player_ship.rect.y+5, -10)
                            bullet4 = Bullet(player_ship.rect.x+93 , player_ship.rect.y+5, -10)
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
                
                # detect bullet sprites that collide with alien sprites, if so the sprides get killed from their group and points are added to the score
                collided_bullets_aliens = pygame.sprite.groupcollide(all_bullets_list, aliens, True, True, False)
                if collided_bullets_aliens.values():
                    for killed_aliens in collided_bullets_aliens.values():
                        for killed_alien in killed_aliens:
                            point_counter+=killed_alien.points

                asteroid_hit = pygame.sprite.groupcollide(all_asteroids_list, all_bullets_list, True, True)
                asteroid_hit = pygame.sprite.groupcollide(all_asteroids_list, all_alien_bullets_list, True, True)
                asteroid_hit = pygame.sprite.groupcollide(all_asteroids_list, aliens, True, False)
                
        
                #lives = pygame.sprite.spritecollide(player_ship, aliens, True)
                #if (pygame.sprite.spritecollideany(player_ship, all_alien_bullets_list)) is not None:
                    
            
                # --- Drawing code --------------------------------------------------------
                
                # drawing all sprites
                self.screen.blit(self.background, (0, 0))
                
                aliens.draw(self.screen)
                all_sprites_list.draw(self.screen)
                

                point_counter_score = pygame.font.SysFont('Consolas', 32).render(str(point_counter), True, pygame.color.Color('White'))
                self.screen.blit(point_counter_score, (100, 100))


                if (pygame.sprite.spritecollideany(player_ship, all_alien_bullets_list) is not None or pygame.sprite.spritecollideany(player_ship, aliens) is not None) and player_ship.got_hit == False:
                    #font = pygame.font.Font(None, 36)
                    #text = font.render("GOT HIT MATE", 1, (255, 255, 255))
                    #self.screen.blit(text, (500,500))
                    player_ship.get_hit()
                    if len(player_life_sprite_list)>=1:
                        all_sprites_list.remove(player_life_sprite_list[-1])
                        player_life_sprite_list = player_life_sprite_list[:-1]
                    else:
                        self.screen.blit(pygame.font.SysFont('Consolas', 64).render("Game Over", True, pygame.color.Color('White')), (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
                        
            elif state == PAUSE:
                self.screen.blit(pause_text, (100, 100))
                self.pause_menu.mainloop(events, disable_loop=test) 
                

        
    
            # refresh screen.
            pygame.display.flip()
            # If test returns
            if test:
                break  
        player = self.player_name_entering(difficulty,point_counter)
        self.highscore= [player,difficulty,point_counter]
        print (self.highscore)
        

 

    def player_name_entering(self,difficulty,point_counter):
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
                        shiftDown = False
                if e.type == pygame.KEYDOWN:
                    textBox.add_chr(pygame.key.name(e.key))
                    if e.key == pygame.K_SPACE:
                        textBox.text += " "
                        textBox.update()
                    if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        shiftDown = True
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

    def save_player_score(self,value):
        """
        This function saves the player score.
        :param value: The widget value
        :type value: basestring
        :return: None
        """
        print('User name: {0}'.format(value))
        print('mode: {0}'.format(self.highscore[0]))
        print('score: {0}'.format(self.highscore[1]))
    

    def create_game_over_menu(self):
        self.game_over_menu = pygameMenu.TextMenu(self.screen,
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
                                    title='Game Over',
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )
        if self.highscore is not None:                            
            self.game_over_menu.add_line('Gamemode: '+str(self.highscore[0]))
            self.game_over_menu.add_line('Score: '+str(self.highscore[1]))                           
        self.game_over_menu.add_text_input('Name: ',
                                        default='Spacer',
                                        onreturn=self.save_player_score,
                                        textinput_id='player_name')
        self.game_over_menu.add_line('----------------------------------------------')  
        self.game_over_menu.add_option('Save Highscore', self.save_player_score,self.game_over_menu.get_input_data())  # Call function
        self.game_over_menu.add_option('Menu', self.main_menu)
        self.game_over_menu.add_option('Quit', pygameMenu.events.EXIT)



    def main(self,test=False,*score):
        """
        Main program.
        :param test: Indicate function is being tested
        :type test: bool
        :return: None
        """
 
        # -------------------------------------------------------------------------
        # Globals
        # -------------------------------------------------------------------------


        # -------------------------------------------------------------------------
        # Create menus
        # -------------------------------------------------------------------------

        # Play menu
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

        self.play_menu.add_option('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                            self.play_function,
                            DIFFICULTY,
                            pygame.font.Font(pygameMenu.font.FONT_FRANCHISE, 30))
        self.play_menu.add_selector('Select difficulty',
                            [('1 - Easy', 'EASY'),
                                ('2 - Medium', 'MEDIUM'),
                                ('3 - Hard', 'HARD')],
                            onchange=self.change_difficulty,
                            selector_id='select_difficulty')
        self.play_menu.add_option('Return to main menu', pygameMenu.events.BACK)

        # About menu
        
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

        HIGHSCORE_LIST = ['1: Tassilo: 500','2: Tassilo: 400','3: Tassilo: 300']
        for line in HIGHSCORE_LIST:
            self.highscore_menu.add_line(line) 
        self.highscore_menu.add_option('Return to Menu', pygameMenu.events.BACK)



        # Main menu
        
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

        self.game_over_menu = pygameMenu.TextMenu(self.screen,
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
                                    title='Game Over',
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )
        if self.highscore is not None:                            
            self.game_over_menu.add_line('Gamemode: '+str(self.highscore[0]))
            self.game_over_menu.add_line('Score: '+str(self.highscore[1]))                           
        self.game_over_menu.add_text_input('Name: ',
                                        default='Spacer',
                                        onreturn=self.save_player_score,
                                        textinput_id='player_name')
        self.game_over_menu.add_line('----------------------------------------------')  
        self.game_over_menu.add_option('Save Highscore', self.save_player_score,self.game_over_menu.get_input_data())  # Call function
        self.game_over_menu.add_option('Menu', self.main_menu)
        self.game_over_menu.add_option('Quit', pygameMenu.events.EXIT)

        
        

        # Configure main menu
        self.main_menu.set_fps(FPS)

        # -------------------------------------------------------------------------
        # Main loop
        # -------------------------------------------------------------------------
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

            # Main menu
            #if (self.highscore is not None):
            #    self.main_menu.enable()
            #self.main_menu.mainloop(events)
            self.main_menu.mainloop(events)

            if (not self.main_menu.is_enabled()):
                self.main_menu.enable()
                       
            #, disable_loop=test)
           # else:
            #    self.main_menu.reset(1)
            #    self.main_menu.mainloop(events,disable_loop=test)
                

            # Flip screen
            pygame.display.flip()

            # At first loop returns
            if test:
                break

if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()