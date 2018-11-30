'''
Game Engine

This handles the updates of surfaces before getting blitted into the main
surface. Event handling for the game
'''
#Main imports
import pygame as pg
import time
import random
import pickle

#Relative imports
from . import entities
from . import constants as C
from . import game


class Engine(object):
    '''Main game engine. Handles the current screen and/or switching screens.'''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.update_rects = []

        self.transition = Transition(self.width, self.height, self)
        self.splash = SplashScreen(self.width, self.height, self)
        self.credits = Credits(self.width, self.height, self)
        self.instructions = Instructions(self.width, self.height, self)
        self.mainmenu = MainMenu(self.width, self.height, self)
        self.game = game.Game(self.width, self.height, self)

        self.se = SoundEffects()
        self.ih = ImageHandler()

        self.active = self.splash
        self.temp_screen = pg.surface.Surface((width, height)).convert()


    def pass_values(self, images, sounds):
        self.se = sounds
        self.ih = images
        #Create all game screens after loading the images/sounds
        self.splash.create()
        self.credits.create()
        self.instructions.create()
        self.mainmenu.create()
        self.game.create()

        
    def update(self, buttons, mouse):
        if self.transition.finished:
            msg = self.active.update(buttons, mouse)
            if msg == 'main_menu':
                self.transition.reset()
                self.active.draw(self.temp_screen)
                self.active = self.mainmenu
            elif msg == 'splash':
                self.transition.reset()
                self.active.draw(self.temp_screen)
                self.active = self.splash
            elif msg == 'credits':
                self.transition.reset()
                self.active.draw(self.temp_screen)
                self.active = self.credits
            elif msg == 'instructions':
                self.transition.reset()
                self.active.draw(self.temp_screen)
                self.active = self.instructions
            elif msg == 'game':
                self.transition.reset()
                self.active.draw(self.temp_screen)
                self.active = self.game
        else:
            self.transition.update(buttons, mouse)
            if self.transition.hidden:
                self.active.update(buttons, mouse)


    def draw(self, screen):
        if self.transition.finished:
            self.active.draw(screen)
        else:
            if self.transition.hidden:
                self.active.draw(screen)
            else:
                screen.blit(self.temp_screen, (0, 0))
            self.transition.draw(screen)


class SoundEffects(object):
    '''Game class that handles sound objects.'''
    def __init__(self):
        self.music_lib = {}


    def add_sound(self, name, audio):
        self.music_lib[name] = audio


    def play(self, name):
        if self.music_lib[name].get_num_channels():
            self.music_lib[name].stop()
            if name  in ['bgm',]: #List contains name of BGMs
                self.music_lib[name].play(-1) #BGM loops infinitely
            else:
                self.music_lib[name].play()


class ImageHandler(object):
    '''Game class that handles all loaded images.'''
    def __init__(self):
        self.image_lib = {}


    def add_image(self, name, image):
        self.image_lib[name] = image


    def get_image(self, name):
        return self.image_lib[name]


class LoadingScreen(object):
    '''Gamme load screen on the start of the game.'''
    def __init__(self, width, height):
        self.image = pg.surface.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.audio_loader = {}
        self.image_loader = {}
        self.audios = []
        self.images = []

        self.loaded = False
        self.loading = pg.surface.Surface((64, 64)).convert()
        self.loading.fill(C.BLACK)
        self.ih = ImageHandler()
        self.se = SoundEffects()
        self.set_loader()
        self.finished = False
        self.last_update = 0


    def set_loader(self):
        '''Reads all the files from the resources.load file.'''
        file = open('Resources/resources.load', 'r')
        file.seek(0)
        all_lines = file.readlines()
        for line in all_lines:
            if line[0] not in ['#', ' ', '\n']:
                args = line.split()
                if args[0].lower() == 'audio':
                    obj, name, path, volume = args
                    self.audio_loader[name] = [path, float(volume)]
                elif args[0].lower() == 'image':
                    obj, name, path = args
                    self.image_loader[name] = path
        file.close()
        self.audios = list(self.audio_loader.keys())
        self.images = list(self.image_loader.keys())
        self.angle = 0


    def load(self, load_type, load_to):
        if load_type == 'image':
            try:
                key = self.images.pop(0)
                image = pg.image.load(self.image_loader[key]).convert_alpha()
                load_to.add_image(key, image)
            except:
                pass
        elif load_type == 'audio':
            try:
                key = self.audios.pop(0)
                audio = pg.mixer.Sound(self.audio_loader[key][0])
                audio.set_volume(self.audio_loader[key][1])
                load_to.add_sound(key, audio)
            except:
                pass


    def update(self):
        self.image.fill(C.BLACK)
        if self.images:
            self.load('image', self.ih)
            self.last_update = pg.time.get_ticks()
        elif self.audios:
            self.load('audio', self.se)
            self.last_update = pg.time.get_ticks()
        else:
            curr_time = pg.time.get_ticks()
            if curr_time - self.last_update > 2000:
                self.finished = True
            
        if not self.loaded:
            try:
                self.loading = self.ih.get_image('loading')
                self.loaded = True
            except:
                pass

        temp = pg.transform.rotate(self.loading, self.angle)
        trect = temp.get_rect(center=self.rect.center)
        self.image.blit(temp, trect)
            
        self.angle = (self.angle - 10)%360
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Transition(object):
    '''Transition screen that plays between switching of screens.'''
    def __init__(self, width, height, engine):
        self.image = pg.surface.Surface((width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.engine = engine
        self.alpha = 0
        self.hidden = False
        self.finished = False

        self.last_update = 0
        

    def update(self, buttons, mouse):
        if not self.hidden and self.alpha < 255:
            self.alpha += 3
            self.last_update = pg.time.get_ticks()
        elif not self.hidden and self.alpha == 255:
            self.hidden = True
        elif self.hidden and self.alpha > 0:
            if pg.time.get_ticks() - self.last_update > 1000:#Stay black for 1s
                self.alpha -= 3
        elif self.hidden and self.alpha == 0:
            self.finished = True
            self.hidden = False
        self.image.fill((0, 0, 0, self.alpha))


    def reset(self):
        self.finished = False

    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

class SplashScreen(object):
    '''Game splash screen that appears after the loading screen.'''
    def __init__(self, width, height, engine):
        self.engine = engine
        self.image = pg.surface.Surface((width, height)).convert()
        self.rect = self.image.get_rect()


    def create(self):
        self.image = self.engine.ih.get_image('banner')
        self.rect = self.image.get_rect()


    def update(self, buttons, mouse):
        if 1 in buttons.values():
            self.finished = True
            return 'instructions'
        else:
            return None


    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Credits(object):
    '''Credit screen.'''
    def __init__(self, width, height, engine):
        self.image = pg.surface.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.engine = engine


    def create(self):
        pass


    def update(self, buttons, mouse):
        self.image.fill(C.GREEN)


    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Instructions(object):
    '''Instructions screen.'''
    def __init__(self, width, height, engine):
        self.image = pg.surface.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.engine = engine


    def create(self):
        pass


    def update(self, buttons, mouse):
        self.image.fill(C.BLUE3)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

class MainMenu(object):
    '''Game's main menu. Handles the main switching of screens.'''
    def __init__(self, width, height, engine):
        self.image = pg.surface.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.engine = engine


    def create(self):
        pass


    def update(self, buttons, mouse):
        self.image.fill(C.YELLOW)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

