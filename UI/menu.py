import os
from pygame import font, Surface, PixelArray

from globals import UPSCALED, vec
from objects import Fading, Drawable, Cursor
from UI import SpriteManager, EventManager, AudioManager

SM = SpriteManager.getInstance()
EM = EventManager.getInstance()
AM = AudioManager.getInstance()

class Title(object):
    """
    This class functions as the engine for the title screen.
    """
    def __init__(self):
        font.init()

        self.display_objects = []
        #   Menu Options    #
        #   States
        self.start_new = False
        self.load = False

        #   Set the font
        fnt = font.Font(os.path.join("UI", "fonts", 'OpenSans-Regular.ttf'), 24)
        self.fnt = fnt
        self.white = (255, 254, 184)
        self.red = (255, 20, 20)

        #   New Game
        text_surface = fnt.render("New Game", True, (255, 254, 184))
        self.display_objects.append([Fading(text_surface, d_a=1, transparent=False), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, UPSCALED[1] // 2 + text_surface.get_height() - 16)])

        #   Load Game
        text_surface = fnt.render("Load Game", True, (255, 254, 184))
        self.display_objects.append([Fading(text_surface, d_a=1, transparent=False), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, (UPSCALED[1] // 2 + (text_surface.get_height()) * 2)- 16)])
        
        #   Quit Game :(
        text_surface = fnt.render("Quit Game", True, (255, 254, 184))
        self.display_objects.append([Fading(text_surface, d_a=1, transparent=False), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, (UPSCALED[1] // 2 + (text_surface.get_height()) * 3) - 16)])

    def initialize(self):
        #   Pointer
        self.pointer = Cursor(vec(0,0), "pointer.png")
        self.pointer.scale_image()

        pos = self.display_objects[0][1].copy()
        pos[0] -= (self.pointer.get_width() + 8)
        pos[1] += (self.pointer.get_height() // 2 - 10)
        self.pointer.set_position(pos)

        text_surface = self.fnt.render("New Game", True, self.red)
        self.display_objects[0][0] = Fading(text_surface, d_a=1, transparent=False)
        
        self.pointer_position = 0 # 0 for new game, 1 for load, 2 for quit

    def draw(self, drawSurf):
        for o in self.display_objects:
            drawSurf.blit(*o)
        
        # self.pointer.draw(drawSurf)
    
    def handle_events(self):
        if EM.perform_action('interact'):
            #   Start a new game
            if self.pointer_position == 0:
                self.start_new = True

            #   Load a game
            elif self.pointer_position == 1:
                self.load = True

            #   Quit the game
            elif self.pointer_position == 2:
                EM.QUIT()

        elif self.pointer_position < 2 and EM.perform_action('motion_down'):
            # AM.playMenuSFX("menu_1.wav")
            # AM.playSFX("menu_1.wav")

            self.pointer_position += 1

            #   Set to Load
            if self.pointer_position == 1:
                pos = self.display_objects[1][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make Load red
                text_surface = self.fnt.render("Load Game", True, self.red)
                self.display_objects[1][0] = Fading(text_surface, d_a=1, transparent=False)

                #   Make New White
                text_surface = self.fnt.render("New Game", True, self.white)
                self.display_objects[0][0] = Fading(text_surface, d_a=1, transparent=False)
            
            #   Set to Quit
            elif self.pointer_position == 2:
                pos = self.display_objects[2][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make Quit red
                text_surface = self.fnt.render("Quit Game", True, self.red)
                self.display_objects[2][0] = Fading(text_surface, d_a=1, transparent=False)

                #   Make Load white
                text_surface = self.fnt.render("Load Game", True, self.white)
                self.display_objects[1][0] = Fading(text_surface, d_a=1, transparent=False)

        elif self.pointer_position > 0 and EM.perform_action('motion_up'):
            # AM.playMenuSFX("menu_1.wav")
            # AM.playSFX("menu_1.wav")
            self.pointer_position -= 1

            #   Set to Load
            if self.pointer_position == 1:
                pos = self.display_objects[1][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make Load Red
                text_surface = self.fnt.render("Load Game", True, self.red)
                self.display_objects[1][0] = Fading(text_surface, d_a=1, transparent=False)
            
                #   Make Quit White
                text_surface = self.fnt.render("Quit Game", True, self.white)
                self.display_objects[2][0] = Fading(text_surface, d_a=1, transparent=False)

            #   Set to New
            elif self.pointer_position == 0:
                pos = self.display_objects[0][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make New Red
                text_surface = self.fnt.render("New Game", True, self.red)
                self.display_objects[0][0] = Fading(text_surface, d_a=1, transparent=False)

                #   Make Load White
                text_surface = self.fnt.render("Load Game", True, self.white)
                self.display_objects[1][0] = Fading(text_surface, d_a=1, transparent=False)

        return
    
    def update(self, seconds):
        for o in self.display_objects:
            o[0].update(seconds)
        
        self.pointer.update(seconds)