# Space Invaders
# Created by Tassilo Henninger

import sys
import pygame
from ship import Ship
from alien import Alien
from bullet import Bullet

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

screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("Space Invaders")
pygame.mouse.set_visible(0)
background = pygame.image.load('images\\background.png').convert()



# list contains all the sprites in the game.
all_sprites_list = pygame.sprite.Group()
# list contains all the aliens in the game.
all_aliens_list = pygame.sprite.Group()
# list contains all the bullets in the game.
all_bullets_list = pygame.sprite.Group()

playerShip = Ship()
playerShip.rect.x = SCREENWIDTH/2 -playerShip.getWidth()/2
playerShip.rect.y = SCREENHEIGHT - playerShip.getHight()

# add the player to the list of objects
all_sprites_list.add(playerShip) 

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
        bullet = Bullet(playerShip.rect.x , playerShip.rect.y, -5)
        all_bullets_list.add(bullet)
        all_sprites_list.add(bullet)
        pygame.mixer.Sound('sounds/shoot.wav').play()
 
    # ------ Game logic -------------------------------------------------------
    all_sprites_list.update()

 
    # --- Drawing code --------------------------------------------------------
    
    # drawing all sprites
    screen.blit(background, (0, 0))

    # Calls update() method on every sprite in the list and draws them
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    
     
    # refresh screen.
    pygame.display.flip()
     
    # 60 fps
    clock.tick(60)
 
#quit game engine:
pygame.quit()


def createAliens(self, numberofaliens):
    for i in numberofaliens:
        alien = Alien()
        alien.rect.x = SCREENWIDTH/2 -alien.getWidth()/2
        alien.rect.y = SCREENHEIGHT - alien.getHight()
        all_sprites_list.add(alien)
        all_aliens_list.add(alien)
     




