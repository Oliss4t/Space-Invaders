import pygame
class TextBox(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.text = ""
            self.font = pygame.font.Font(None, 50)
            self.image = self.font.render("Enter your name", False, [0, 0, 0])
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
            self.image = self.font.render(self.text, False, [0, 0, 0])
            self.rect = self.image.get_rect()
            self.rect.center = old_rect_pos