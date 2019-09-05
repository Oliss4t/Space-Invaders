# Space Invaders
# Created by Tassilo Henninger

import sys
import pygame
import pygame-menu
from ship import Ship
from alien import Alien
from bullet import Bullet
from aliengroup import AlienGroup

# initialise the game engine
pygame.init()

# defintion of the used colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

# open the main window
SCREEN_WIDTH=1200
SCREEN_HEIGHT=900
ALIEN_DEFAULT_POSITION= 50
ALIEN_DEFAULT_HIGHT= 87
ALIEN_DEFAULT_WIDTH=64


menu = pygameMenu.Menu(surface, SCREEN_WIDTH, SCREEN_HEIGHT)
menu.add_option(timer_menu.get_title(), timer_menu)         # Add timer submenu
menu.add_option(help_menu.get_title(), help_menu)           # Add help submenu
menu.add_option(about_menu.get_title(), about_menu)         # Add about submenu
menu.add_option('Exit', pygameMenu.events.MENU_EXIT) # Add exit function

# list contains all the sprites in the game.
all_sprites_list = pygame.sprite.Group()
# list contains all the aliens in the game.
all_aliens_list = pygame.sprite.Group()
# list contains all the bullets in the game.
all_bullets_list = pygame.sprite.Group()

all_alien_bullets_list =pygame.sprite.Group()

#def createAliens(numbersofrows, numberofaliensinrow):
#    for i in range(numbersofrows):
#        for ii in range(numberofaliensinrow):
#            alien = Alien(SCREEN_WIDTH,SCREEN_HEIGHT)
#            alien.rect.x = 50 + ii* 100
#            alien.rect.y = 50 + i* 90
#            all_sprites_list.add(alien) 
#            all_aliens_list.add(alien)


#make_aliens(11,5)
def make_aliens(columns,rows):
    #calculate the space, that all aliens are allined
    devided_space =(SCREEN_WIDTH-2*ALIEN_DEFAULT_POSITION)/columns
    aliens = AlienGroup(columns, rows, devided_space, SCREEN_WIDTH)
    for row in range(rows):
        for column in range(columns):
            alien = Alien(SCREEN_WIDTH,SCREEN_HEIGHT,row, column)
            alien.rect.x = ALIEN_DEFAULT_POSITION + ((column-1) * devided_space)
            alien.rect.y = ALIEN_DEFAULT_POSITION + ((row-1) * ALIEN_DEFAULT_HIGHT )
            aliens.add(alien)
#    self.enemies = enemies

def make_enemies_shoot(self):
    if (time.get_ticks() - self.timer) > 700 and self.enemies:
        enemy = self.enemies.random_bottom()
        self.enemyBullets.add(
            Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5,
                    'enemylaser', 'center'))
        self.allSprites.add(self.enemyBullets)
        self.timer = time.get_ticks()


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
pygame.mouse.set_visible(0)
background = pygame.image.load('images\\background.png').convert()

# creat and add the player to the list of objects
player_ship = Ship()
player_ship.rect.x = SCREEN_WIDTH/2 -player_ship.get_width()/2
player_ship.rect.y = SCREEN_HEIGHT - player_ship.get_hight()
all_sprites_list.add(player_ship) 

#create aliens
#make_aliens(11,5)
columns=8
rows=3
devided_space =(SCREEN_WIDTH-2*ALIEN_DEFAULT_POSITION)/columns
aliens = AlienGroup(columns, rows, devided_space, SCREEN_WIDTH)
for row in range(rows):
    for column in range(columns):
        alien = Alien(SCREEN_WIDTH,SCREEN_HEIGHT,row, column)
        alien.rect.x = ALIEN_DEFAULT_POSITION + ((column) * devided_space)
        alien.rect.y = ALIEN_DEFAULT_POSITION + ((row) * ALIEN_DEFAULT_HIGHT )
        aliens.add(alien)
aliens.init_bottom_aliens()

# flag for continuing the game
carry_on = True
# the clock controls fps
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while carry_on:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carry_on = False # flag for exiting the game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:# If user presses escape
                carry_on = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_ship.move_left(SCREEN_WIDTH/100,SCREEN_WIDTH)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_ship.move_right(SCREEN_WIDTH/100,SCREEN_WIDTH)
    if keys[pygame.K_SPACE]:
        if not all_bullets_list:
            ################################################################################# to implement
            if (False):#level 1
                bullet = Bullet(player_ship.rect.x+70 , player_ship.rect.y+20, -10)
                all_bullets_list.add(bullet)
                all_sprites_list.add(bullet)
                pygame.mixer.Sound('sounds/shoot.wav').play()
            if (True):#level 2
                bullet1 = Bullet(player_ship.rect.x+49 , player_ship.rect.y+5, -10)
                bullet2 = Bullet(player_ship.rect.x+83 , player_ship.rect.y+5, -10)
                all_bullets_list.add(bullet1,bullet2)
                all_sprites_list.add(bullet1,bullet2)
                pygame.mixer.Sound('sounds/shoot.wav').play()

 
    # ------ Game logic -------------------------------------------------------
    # Calls update() method on every sprite in the list 
    alien_bullet = aliens.random_shoot()
    if alien_bullet is not None:
        all_sprites_list.add(alien_bullet)
        all_alien_bullets_list.add(alien_bullet)
    all_sprites_list.update()
    aliens.update()
    
    # Find all sprites that collide between two groups and kills them from their group
    alien_hit_list = pygame.sprite.groupcollide(all_bullets_list, aliens, True, True, False)
    
    lives = pygame.sprite.spritecollide(player_ship, aliens, True)
    #if (pygame.sprite.spritecollideany(player_ship, all_alien_bullets_list)) is not None:
        
 
    # --- Drawing code --------------------------------------------------------
    
    # drawing all sprites
    screen.blit(background, (0, 0))
    all_sprites_list.draw(screen)
    aliens.draw(screen)

    if (pygame.sprite.spritecollideany(player_ship, all_alien_bullets_list)) is not None:
        font = pygame.font.Font(None, 36)
        text = font.render("GOT HIT MATE", 1, (255, 255, 255))
        screen.blit(text, (500,500))
    
     
    # refresh screen.
    pygame.display.flip()
     
    # 60 fps
    clock.tick(60)
 
#quit game engine:
pygame.quit()

