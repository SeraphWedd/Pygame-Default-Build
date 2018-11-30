'''
Game

This file contains the main game.
'''
#Main imports
import pygame as pg

#Relative imports
from . import entities
from . import constants as C


class Game(object):
    '''This is the main game logic handler.'''
    def __init__(self, width, height, engine):
        self.image = pg.surface.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.engine = engine


    def create(self):
        pass


    def update(self, buttons, mouse):
        pass


    def draw(self, screen):
        screen.blit(self.image, self.rect)
