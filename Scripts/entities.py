'''
Entities

This contains all pygame elements that is present in the game.
'''
#Main Imports
import pygame as pg

#Relative imports
from . import methods


class Mouse(pg.sprite.Sprite):
    '''Mouse object responsible for mouse collision detection.'''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.surface.Surface((16, 16)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.values = [(0, 0),#Mouse Pos
                       0,#Left Click
                       0,#Middle Click
                       0,#Right Click
                       ]
        self.update_rects = [self.rect]
        
        #you can load a static or an Animated image for the mouse
        #This is a sample image only
        pg.mouse.set_visible(False)
        self.press_image = [self.image.convert_alpha()]
        self.release_image = [self.image.convert_alpha()]
        self.is_animated = False

        self.last_update = 0
        self.index = 0
        self.len = 1


    def load_mouse_image(self, is_animated, pressed, released):
        '''Loads the images to be used for the mouse.
Pressed and released is a list of surfaces if is_animated.
'''
        
        self.is_animated = is_animated
        if self.is_animated:
            self.press_image = pressed
            self.release_image = released
            self.len = len(self.press_image)
        else:
            self.press_image = [pressed]
            self.release_image = [released]
            

    def set_values(self, index, value):
        if index: #Click
            self.values[index] = value
        else: #Motion
            self.values[index] = value
            self.update_rects = [pg.rect.Rect(self.rect)] #Add prev rect
            self.rect.topleft = value #Can set to center or topleft
            self.update_rects.append(self.rect) #Add curr rect


    def update(self):
        curr_time = pg.time.get_ticks()
        if curr_time - self.last_update > 100:
            self.last_update = curr_time
            self.index = (self.index + 1)%self.len

        if self.values[1]:
            self.image = self.press_image[self.index]
        else:
            self.image = self.release_image[self.index]


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return self.update_rects


class Button(pg.sprite.Sprite):
    '''Base button class.'''
    def __init__(self, text, size, pos):
        pg.sprite.Sprite.__init__(self)
        self.text = text
        self.size = size
        self.font = pg.font.SysFont('Times', self.size)
        self.color = (20, 20, 20)
        self.image, self.rect = methods.make_text_object(
            self.text, self.font, self.color)
        self.rect.center = pos
        self.clicked = False

        self.press_image = self.image.convert()
        self.release_image = self.image.convert()

    def load_button_image(self, pressed, released):
        self.press_image = pressed
        self.release_image = released


    def update(self, buttons, mouse):
        if pg.sprite.collide_rect(self, mouse):
            if mouse.values[1] and not self.clicked: #On left click
                self.clicked = True
            elif not mouse.values[1] and self.clicked: #Execute on release
                #Do something
                self.clicked = False
        if self.clicked:
            self.image = self.press_image
        else:
            self.image = self.release_image
                
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

