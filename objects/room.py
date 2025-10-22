from math import ceil
import os

from pygame import Surface

from . import Player, Drawable, TextManager, EventManager
from globals import SCREEN_SIZE, UPSCALED, SCALE_FACTOR, vec
from UI import SpriteManager

SM = SpriteManager.getInstance()
TM = TextManager.getInstance()
EM = EventManager.getInstance()


class Room(object):
    def __init__(self):
        self.size = vec(UPSCALED[0] * 20, UPSCALED[1])
        self.player = Player()
        self.player.set_position(vec(UPSCALED[0] // 2 - self.player.get_width() // 2, UPSCALED[1] - UPSCALED[1] // 4 - self.player.get_height()))
        
        #   States  #
        self.speaking = False # in dialogue

        #   Art #
        self.background = []
        num_images = ceil(self.size[0] / 320)
        num_rows = 2

        for i in range(0, num_images + 1):
            for j in range(num_rows):
                self.background.append(Drawable(vec(i*320,j*180), os.path.join("sunset","background.png")))
       
        self.layers = []
        for i in range(0,num_images+1):
            for j in range(1,num_rows):
                for k in range(1,4):
                    string = str(k) + '.png'
                    self.layers.append(Drawable(vec(i*320,j*180), os.path.join("sunset", string)))

        self.foreground = []
        # for i in range(0,num_images):
        #     for j in range(1,num_rows):
        #         self.foreground.append(Drawable(vec(i*320,j*180), os.path.join("sunset","foreground.png")))
            
        Drawable.updateOffset(self.player, self.size)

    def draw(self, drawSurf):
        for b in self.background:
            b.draw(drawSurf)

        for l in self.layers:
            l.draw(drawSurf)

        bbg = Surface((SCREEN_SIZE[0] * 4, 1))
        bbg.fill((230,0,0))
        drawSurf.blit(bbg, vec(0, SCREEN_SIZE[1] // 4))

        bg = Surface((SCREEN_SIZE[0] * 4, 1))
        bg.fill((0,0,0))
        drawSurf.blit(bg, vec(0, SCREEN_SIZE[1] // 2))

        #   Player  #
        self.player.draw(drawSurf)
        
        #   Foreground  #
        for f in self.foreground:
            f.draw(drawSurf)
        fg = Surface((SCREEN_SIZE[0] * 4, 1))
        fg.fill((0,200,0))
        drawSurf.blit(fg, vec(0, SCREEN_SIZE[1] - SCREEN_SIZE[1] // 4))

        #   Dialogue    #
        if self.speaking:
            TM.draw(drawSurf)

    def handle_events(self):
        if self.speaking:
            TM.handle_events()

        else:
            if EM.perform_action('space'):
                txt = "Greetings.&&\nWelcome to reverie.$$It's been a while,\nhuh?$$Today I've got a pocket\nfull of chimp change.$$Glorious day."
                self.display_text(txt)
            
            else:
                self.player.handle_events()
    
    def display_text(self, text="Hello", flag = 0):
        self.speaking = True
        TM.init(text, flag)
    
    def update(self, seconds):
        self.player.update(seconds)
        Drawable.updateOffset(self.player, self.size)

        if self.speaking:
            TM.update(seconds)

            if TM.is_finished():
                TM.reset()
                self.speaking = False
