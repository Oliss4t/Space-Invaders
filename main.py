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

    def play_function(self,difficulty, font, test=False):

        point_counter = 0
        player_lvl =1
        assert isinstance(difficulty, (tuple, list))
        difficulty = difficulty[0]
        assert isinstance(difficulty, str)

  
        if difficulty == 'EASY':
            f = font.render('Playing as a baby (easy)', 1, COLOR_WHITE)
        elif difficulty == 'MEDIUM':
            f = font.render('Playing as a kid (medium)', 1, COLOR_WHITE)
        elif difficulty == 'HARD':
            f = font.render('Playing as a champion (hard)', 1, COLOR_WHITE)
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
        
        all_asteroids_list = self.make_asteroid(10,100,60,4,COLOR_GREY)
        #all_asteroids_list = pygame.sprite.Group()
        asteroids= create_asteroid_ellipse3(1,100,600,300,700,COLOR_WHITE,False)
        all_asteroids_list.add(asteroids)

        all_sprites_list.add(all_asteroids_list)

        # creat and add the player to the list of objects
        player_ship =self.load_player(0,0,1)
        all_sprites_list.add(player_ship) 

        #create aliens
        aliens=self.make_aliens(8,3,[3,2,1])

        

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
        while True:
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
                
        
                lives = pygame.sprite.spritecollide(player_ship, aliens, True)
                #if (pygame.sprite.spritecollideany(player_ship, all_alien_bullets_list)) is not None:
                    
            
                # --- Drawing code --------------------------------------------------------
                
                # drawing all sprites
                self.screen.blit(self.background, (0, 0))
                all_sprites_list.draw(self.screen)
                aliens.draw(self.screen)
                point_counter_score = pygame.font.SysFont('Consolas', 32).render(str(point_counter), True, pygame.color.Color('White'))
                self.screen.blit(point_counter_score, (100, 100))


                if (pygame.sprite.spritecollideany(player_ship, all_alien_bullets_list)) is not None:
                    font = pygame.font.Font(None, 36)
                    text = font.render("GOT HIT MATE", 1, (255, 255, 255))
                    self.screen.blit(text, (500,500))
            elif state == PAUSE:
                self.screen.blit(pause_text, (100, 100))
                self.pause_menu.mainloop(events, disable_loop=test) 
                

        
    
            # refresh screen.
            pygame.display.flip()
            # If test returns
            if test:
                break  


    def main_background(self):
        """
        Function used by menus, draw on background while menu is active.
        :return: None
        """
        self.screen.blit(self.background, (0, 0))


    def main(self,test=False):
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
        self.play_menu.add_option('Another menu', self.play_submenu)
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
        self.main_menu.add_option('Quit', pygameMenu.events.EXIT)


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
            self.main_menu.mainloop(events, disable_loop=test)

            # Flip screen
            pygame.display.flip()

            # At first loop returns
            if test:
                break

if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()