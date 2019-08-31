
clock = pygame.time.Clock() 

# display settings
screen = pygame.display.set_mode((800,600))
pygame.mouse.set_visible(0)

# loading images for visuals 
ship = pygame.image.load('images\shiplvl1.png').convert()

#positions
ship_top = screen.get_height() - ship.get_hight()
ship_left = screen.width()/2 - ship.get_width()/2

screen.blit(ship, (ship_top,ship_left))

while True:
    clock.tick(60)
    pygame.display.update()

    # check for exit the game
    for event in event.get():
        if event.type == pygame.QUIT:
            sys.exit()
