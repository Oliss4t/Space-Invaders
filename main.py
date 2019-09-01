# Space Invaders
# Created by Tassilo Henninger

import sys
import pygame
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
SCREENWIDTH=1200
SCREENHEIGHT=900
ALIENDEFAULTPOSITION= 50
ALIENDEFAULTHIGHT= 87
ALIENDEFAULTWIDTH=64

# list contains all the sprites in the game.
all_sprites_list = pygame.sprite.Group()
# list contains all the aliens in the game.
all_aliens_list = pygame.sprite.Group()
# list contains all the bullets in the game.
all_bullets_list = pygame.sprite.Group()

#def createAliens(numbersofrows, numberofaliensinrow):
#    for i in range(numbersofrows):
#        for ii in range(numberofaliensinrow):
#            alien = Alien(SCREENWIDTH,SCREENHEIGHT)
#            alien.rect.x = 50 + ii* 100
#            alien.rect.y = 50 + i* 90
#            all_sprites_list.add(alien) 
#            all_aliens_list.add(alien)


#make_aliens(11,5)
def make_aliens(ccolumns,crows):
    #calculate the space, that all aliens are allined
    devided_space =(SCREENWIDTH-2*ALIENDEFAULTPOSITION)/ccolumns
    aliens = AlienGroup(ccolumns, crows, devided_space, SCREENWIDTH)
    for row in range(crows):
        for column in range(ccolumns):
            alien = Alien(SCREENWIDTH,SCREENHEIGHT,row, column)
            alien.rect.x = ALIENDEFAULTPOSITION + ((column-1) * devided_space)
            alien.rect.y = ALIENDEFAULTPOSITION + ((row-1) * ALIENDEFAULTHIGHT )
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


screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("Space Invaders")
pygame.mouse.set_visible(0)
background = pygame.image.load('images\\background.png').convert()

# creat and add the player to the list of objects
playerShip = Ship()
playerShip.rect.x = SCREENWIDTH/2 -playerShip.getWidth()/2
playerShip.rect.y = SCREENHEIGHT - playerShip.getHight()
all_sprites_list.add(playerShip) 

#create aliens
#make_aliens(11,5)
ccolumns=8
crows=3
devided_space =(SCREENWIDTH-2*ALIENDEFAULTPOSITION)/ccolumns
aliens = AlienGroup(ccolumns, crows, devided_space, SCREENWIDTH)
for row in range(crows):
    for column in range(ccolumns):
        alien = Alien(SCREENWIDTH,SCREENHEIGHT,row, column)
        alien.rect.x = ALIENDEFAULTPOSITION + ((column) * devided_space)
        alien.rect.y = ALIENDEFAULTPOSITION + ((row) * ALIENDEFAULTHIGHT )
        aliens.add(alien)


# flag for continuing the game
carryOn = True
# the clock controls fps
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # flag for exiting the game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:# If user presses escape
                carryOn = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerShip.moveLeft(SCREENWIDTH/100,SCREENWIDTH)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerShip.moveRight(SCREENWIDTH/100,SCREENWIDTH)
    if keys[pygame.K_SPACE]:
        if not all_bullets_list:
            ################################################################################# to implement
            if (False):#level 1
                bullet = Bullet(playerShip.rect.x+70 , playerShip.rect.y+20, -10)
                all_bullets_list.add(bullet)
                all_sprites_list.add(bullet)
                pygame.mixer.Sound('sounds/shoot.wav').play()
            if (True):#level 2
                bullet1 = Bullet(playerShip.rect.x+49 , playerShip.rect.y+5, -10)
                bullet2 = Bullet(playerShip.rect.x+83 , playerShip.rect.y+5, -10)
                all_bullets_list.add(bullet1,bullet2)
                all_sprites_list.add(bullet1,bullet2)
                pygame.mixer.Sound('sounds/shoot.wav').play()

 
    # ------ Game logic -------------------------------------------------------
    # Calls update() method on every sprite in the list 
    all_sprites_list.update()
    aliens.update()
    # Find all sprites that collide between two groups and kills them from their group
    alien_hit_list = pygame.sprite.groupcollide(all_bullets_list, aliens, True, True, False)


 
    # --- Drawing code --------------------------------------------------------
    
    # drawing all sprites
    screen.blit(background, (0, 0))
    all_sprites_list.draw(screen)
    aliens.draw(screen)
    
     
    # refresh screen.
    pygame.display.flip()
     
    # 60 fps
    clock.tick(60)
 
#quit game engine:
pygame.quit()







