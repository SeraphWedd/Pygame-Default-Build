'''
Game Loop

Handles the main game's loop including screen updates and events.
This is a linear loop that handles each event one at a time.
Multithreading not yet supported.
'''


#Main imports
import pygame as pg
import os, sys, time

#Local scripts
from Scripts import engine
from Scripts import methods
from Scripts.entities import Mouse


class GameLoop(object):
    '''
This is the main game loop. It covers all the updates for themain screen.
''' 
    def __init__(self):
        #Center the game window
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pg.init()

        self.config = methods.configuration()
        self.width = self.config['width']
        self.height = self.config['height']
        self.screen = pg.display.set_mode((self.width, self.height),
            pg.HWSURFACE|pg.DOUBLEBUF)
        
        self.timer = pg.time.Clock()
        self.fps = self.config['fps']
        self.debugging = self.config['debug']
        self.running = True
        
        self.engine = engine.Engine(self.width, self.height)
        self.loading = engine.LoadingScreen(self.width, self.height)

        self.events = [
            pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN,
            pg.MOUSEBUTTONUP, pg.MOUSEMOTION
            ]
        self.buttons = {
            pg.K_UP:0, pg.K_DOWN:0, pg.K_LEFT:0, pg.K_RIGHT:0,
            pg.K_SPACE:0, pg.K_LALT:0, pg.K_F4:0, pg.K_ESCAPE:0,
            pg.K_RETURN:0, pg.K_w:0, pg.K_a:0, pg.K_s:0, pg.K_d:0,
            }
        
        self.button_keys = self.buttons.keys()
        self.mouse = Mouse()
        
        self.update_rects = [] #


    def run(self):
        #Load first
        while not self.loading.finished:
            self.loading.update()
            self.loading.draw(self.screen)
            self.timer.tick_busy_loop(self.fps)
            pg.display.update()

        self.engine.pass_values(self.loading.ih, self.loading.se)
        self.mouse.load_mouse_image(
            False, self.loading.ih.get_image('mouse_active'),
            self.loading.ih.get_image('mouse_inactive'))
        pg.display.set_caption('game title') #
        pg.display.set_icon(self.loading.ih.get_image('icon'))#
        #Main Loop
        while self.running:
            self.update_rects = []
            #Pygame Event Handling
            self.screen.fill((255, 255, 255))
            for event in pg.event.get(self.events):
                if event.type == pg.QUIT or (
                    self.buttons[pg.K_LALT] and self.buttons[pg.K_F4]):
                    self.quit()
                    
                elif event.type == pg.KEYDOWN:
                    if event.key in self.button_keys:
                        self.buttons[event.key] = 1
                        
                elif event.type == pg.KEYUP:
                    if event.key in self.button_keys:
                        self.buttons[event.key] = 0
                        
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button in [1, 3]:
                        self.mouse.set_values(event.button, 1)
                
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button in [1, 3]:
                        self.mouse.set_values(event.button, 0)

                elif event.type == pg.MOUSEMOTION:
                    self.mouse.set_values(0, event.pos)
                    
                self.debug()#
            pg.event.clear()#Clear event to prepare for next loop

            #Update game elements
            self.timer.tick_busy_loop(self.fps)
            self.engine.update(self.buttons, self.mouse)
            self.mouse.update()

            #Draw Elements to screen
            self.engine.draw(self.screen)
            self.mouse.draw(self.screen)

            #Update display
            pg.display.update()#self.update_rects)

##            #Check if display is active (not minimized)
##            if pg.display.get_active():
##                pass
                

    def quit(self):
        pg.quit()
        sys.exit()


    def debug(self):
        '''Prints the current button and mouse values for each event.'''
        #Only for development as it slows the game greatly
        if self.debugging:
            print(self.buttons)
            print(self.mouse.values)


if __name__ == "__main__":
    game = GameLoop()
    game.run()
    
