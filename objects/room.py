from math import ceil
import os

from pygame import Surface

from . import Player, Drawable, TextManager, Interactable
from .enemy import *

from globals import SCREEN_SIZE, UPSCALED, SCALE_FACTOR, vec
from UI import SpriteManager, AudioManager, EventManager

SM = SpriteManager.getInstance()
TM = TextManager.getInstance()
EM = EventManager.getInstance()
AM = AudioManager.getInstance()

class Tile(Drawable):
    """Basic tile. No Collsion"""
    def __init__(self, position, file_name, offset, size = vec(16,16), property = 0):
        self.image = SM.getSprite(os.path.join("tiles", file_name), offset)
        self.position = position
        self.size = size
        self.property = property

    def draw(self, drawSurf):
        drawSurf.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))

class Room(object):
    def __init__(self):
        self.size = vec(UPSCALED[0] * 20, UPSCALED[1])
        self.player = Player()
        self.floor = UPSCALED[1] - UPSCALED[1] // 4
        self.player.set_position(vec(UPSCALED[0] // 2 - self.player.get_width() // 2, UPSCALED[1] - UPSCALED[1] // 4 - self.player.get_height()))
        
        #   BGM #
        self.bgm = "02"
        self.bgm_volume = 2
        self.playing_bgm = False

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
            
        Drawable.updateOffsetPos(self.player.cam_pos, self.size)

        #   Lists of objects in the room    #
        self.npcs = [
            Interactable(vec(self.player.position[0] + 64, self.floor))
        ]
        self.npcs[0].position[1] -= self.npcs[0].get_height()

        self.enemies = [
            Raven(vec(16*8, self.floor))
        ]
        self.unloaded_enemies = []
        #   Camera  #

        #   Tiles   #
        self.tiles = []

        for x in range(0, int(self.size[0]), 16):
            for y in range(int(self.floor) + 16, int(self.size[1]), 16):
                self.tiles += [
                    Tile(vec(x, y), "mid.png", (0,0))
                ]

            self.tiles += [
                Tile(vec(x, self.floor-16), "mid.png", (2,0)),
                Tile(vec(x, self.floor), "mid.png", (2,1))
                ]

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


        #   Npcs    #
        for n in self.npcs:
            n.draw(drawSurf)

        #   Player  #
        self.player.draw(drawSurf)

        #   Enemies #
        for e in self.enemies:
            e.draw(drawSurf)

        #   Foreground  #
        for f in self.foreground:
            f.draw(drawSurf)
        fg = Surface((SCREEN_SIZE[0] * 4, 1))
        fg.fill((0,200,0))
        drawSurf.blit(fg, vec(0, SCREEN_SIZE[1] - SCREEN_SIZE[1] // 4))

        for t in self.tiles:
            t.draw(drawSurf)

        #   Dialogue    #
        if self.speaking:
            TM.draw(drawSurf)

    def handle_events(self):
        if self.speaking:
            TM.handle_events()
        else:
            #   Test Dialogue   #
            if EM.perform_action('space'):
                txt = "Greetings.&&\nWelcome to reverie.$$It's been a while,\nhuh?$$Today I've got a pocket\nfull of chimp change.$$Glorious day."
                self.display_text(txt, row=0)

            #   Interact with an object #
            elif EM.is_active('interact') and not self.player.airborn:
                #   Check if the player can interact with any objects
                for n in self.npcs:
                    if self.player.get_collision_rect().colliderect(n.get_interaction_rect()):
                        self.display_text(n.get_text(), n.get_box())
                        EM.deactivate('interact')
                        return
                self.player.handle_events()

            #   Have the player handle events   #
            else:
                self.player.handle_events()
    
    def display_text(self, text="Hello", flag = 0, row = 0):
        self.player.set_idle()
        self.speaking = True
        TM.init(text, flag, row=row)
    
    def play_bgm(self):
        AM.play_ost(self.bgm, volume=self.bgm_volume)
        self.playing_bgm = True

    def update(self, seconds):
        if not self.playing_bgm:
            self.play_bgm()

        for e in self.enemies:
            e.update(seconds)

        self.player.update(seconds)
        Drawable.updateOffsetPos(self.player.cam_pos, self.size)

        if self.speaking:
            TM.update(seconds)

            if TM.is_finished():
                TM.reset()
                self.speaking = False


        percent = (abs(self.player.vel[0]) / self.player.max_speed)
        if percent > 0.5:
            AM.drum_channel.set_volume(percent)
        else:
            AM.drum_channel.set_volume(0.5)