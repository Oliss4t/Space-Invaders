import pygame
class TextBox(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.text = ""
            self.font = pygame.font.SysFont('Consolas', 64)
            self.image = self.font.render("Enter your name", True, pygame.color.Color('White'))
            self.rect = self.image.get_rect()
            self.shiftDown = False
            self.validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
            self.shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

        def add_chr(self, char):
            self.shiftDown
            if char in self.validChars and not self.shiftDown:
                self.text += char
            elif char in self.validChars and self.shiftDown:
                self.text += self.shiftChars[self.validChars.index(char)]
            self.update()

        def update(self):
            old_rect_pos = self.rect.center
            self.image = self.font.render(self.text,True, pygame.color.Color('White'))
            self.rect = self.image.get_rect()
            self.rect.center = old_rect_pos