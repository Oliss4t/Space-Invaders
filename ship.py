import pygame

class Ship(pygame.sprite.Sprite):
    #This class represents a ship. It derives from the "Sprite" class in Pygame.
    
    def __init__(self,level):
        super().__init__()
        # Draw the ship
        if level ==1:
            self.images = [pygame.transform.scale(pygame.image.load("images\\shiplvl1.png").convert_alpha(), (111, 93)),pygame.transform.scale(pygame.image.load("images\\shiplvl1_explosion1.png").convert_alpha(), (111, 93)),pygame.transform.scale(pygame.image.load("images\\shiplvl1_explosion2.png").convert_alpha(), (111, 93))]
        if level ==2:
            self.images = [pygame.transform.scale(pygame.image.load("images\\shiplvl2.png").convert_alpha(), (111, 93)),pygame.transform.scale(pygame.image.load("images\\shiplvl2_explosion1.png").convert_alpha(), (111, 93)),pygame.transform.scale(pygame.image.load("images\\shiplvl2_explosion2.png").convert_alpha(), (111, 93))]
        if level ==3:
            self.images = [pygame.transform.scale(pygame.image.load("images\\shiplvl3.png").convert_alpha(), (111, 93)),pygame.transform.scale(pygame.image.load("images\\shiplvl3_explosion1.png").convert_alpha(), (111, 93)),pygame.transform.scale(pygame.image.load("images\\shiplvl3_explosion2.png").convert_alpha(), (111, 93))]
        # level_id for the ship-"evolvement" 
        self.image = self.images[0]
        self.level = level
        self.width= self.image.get_size()[0]
        self.hight= self.image.get_size()[1]
        # Fetch a rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.got_hit =False
        self.death_timer = 0
        self.death_animation_toggle =1

    def update(self):
        if self.got_hit:
            self.death_timer += 1
            if self.death_timer % 10 ==0:
                self.image = self.images[self.death_animation_toggle]
                if self.death_animation_toggle == 1:
                    self.death_animation_toggle +=1
                else: 
                    self.death_animation_toggle -=1
            if self.death_timer >= 120:
                self.got_hit =False
                self.death_timer = 0
                self.image = self.images[0]
            

    def get_hit(self):
        self.got_hit = True
            
    def get_hight(self):
        return self.hight

    def get_width(self):
        return self.width

    # move ship right
    def move_right(self, pixels, screen_width):
        if (self.rect.x + pixels) <= (screen_width - self.width):
            self.rect.x += pixels
    
    # move ship left
    def move_left(self, pixels, screen_width):
        if (self.rect.x - pixels) >= 0:
            self.rect.x -= pixels
    
    # shoot bullet/s based on the current level of the ship
    def shoot(self):
        pass
