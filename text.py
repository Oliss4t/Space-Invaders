import pygame

class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = textFont
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)