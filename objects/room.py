from math import ceil
import os

from pygame import Surface, SRCALPHA

from . import Player, Drawable, TextManager, Interactable
from .enemy import *

from globals import SCREEN_SIZE, UPSCALED, SCALE_FACTOR, vec, SPEECH
from UI import SpriteManager, AudioManager, EventManager

SM = SpriteManager.getInstance()
TM = TextManager.getInstance()
EM = EventManager.getInstance()
AM = AudioManager.getInstance()

class RoomManager(object):
    CURRENT_ROOM = None

    def set_next_room(self, room):
        del RoomManager.CURRENT_ROOM
        RoomManager.CURRENT_ROOM = room()
    
    def get_current_room(self):
        return RoomManager.CURRENT_ROOM
    
    
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
    def __init__(self, bgm="02", vol=2):
        self.size = vec(UPSCALED[0] * 20, UPSCALED[1])
        self.player = Player()
        self.floor = UPSCALED[1] - UPSCALED[1] // 4
        self.player.set_position(vec(UPSCALED[0] // 2 - self.player.get_width() // 2, UPSCALED[1] - UPSCALED[1] // 4 - self.player.get_height()))
        
        #   BGM #
        self.bgm = bgm
        self.bgm_volume = vol
        self.playing_bgm = False

        #   States  #
        self.speaking = False # in dialogue
        self.in_cutscene = False
        self.ready_to_transition = False
        self.next_room = Mid_1

        #   Cutscene control    #
        self.text_int = 0
        Drawable.updateOffsetPos(self.player.cam_pos, self.size)
        self.timer = 0.0

        #   Art #
        self.background = []
        self.foreground = []

        #   Lists of objects in the room    #
        self.npcs = []
        self.enemies = []
        self.unloaded_enemies = []

        #   Tiles   #
        self.tiles = []


    def draw(self, drawSurf):
        for b in self.background:
            b.draw(drawSurf)

        # bbg = Surface((SCREEN_SIZE[0] * 4, 1))
        # bbg.fill((230,0,0))
        # drawSurf.blit(bbg, vec(0, SCREEN_SIZE[1] // 4))

        # bg = Surface((SCREEN_SIZE[0] * 4, 1))
        # bg.fill((0,0,0))
        # drawSurf.blit(bg, vec(0, SCREEN_SIZE[1] // 2))


        #   Npcs    #
        for n in self.npcs:
            n.draw(drawSurf)

        #   Enemies #
        for e in self.enemies:
            e.draw(drawSurf)

        #   Player  #
            self.player.draw(drawSurf)

        #   Foreground  #
        for f in self.foreground:
            f.draw(drawSurf)
            
        # fg = Surface((SCREEN_SIZE[0] * 4, 1))
        # fg.fill((0,200,0))
        # drawSurf.blit(fg, vec(0, SCREEN_SIZE[1] - SCREEN_SIZE[1] // 4))

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
        AM.play_ost(self.bgm, volume=self.bgm_volume, play_drums=False, play_intro = True)
        self.playing_bgm = True

    def update(self, seconds, play_music = True, update_bgm = True):
        if play_music and not self.playing_bgm:
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

        if self.in_cutscene:
            return

        if update_bgm:
            percent = (abs(self.player.vel[0]) / self.player.max_speed)
            if percent > 0.1:
                AM.drum_channel.set_volume(percent)
            else:
                AM.drum_channel.set_volume(0.1)







class Mid_1(Room):
    def __init__(self):
        super().__init__(bgm="02")

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
    
    def play_bgm(self):
        AM.play_ost(self.bgm, volume=self.bgm_volume, play_drums=True, play_intro = False)
        self.playing_bgm = True

class Intro(Room):
    def __init__(self):
        super().__init__(bgm="05")
        self.bk = Drawable(vec(0,0), "space.png")
        self.earth = Drawable(vec(SCREEN_SIZE[0] // 2 + 64, 80), "celestial.png", (3,1))
        self.in_cutscene = True
        # self.next_room = Name
        self.next_room = Mid_1

        self.text_int = -1

        #   Lists of objects in the room    #
        #   Interactable Npcs
        self.npcs = [
        ]
        
        #   Enemies
        self.enemies = [
        ]

        #   Unloaded Enemies
        self.unloaded_enemies = []

        #   Tiles
        self.tiles = []
    
    def play_bgm(self):
        """How to properly fade out song and stop playing intro"""
        AM.play_ost(self.bgm, volume=1.0, play_drums=False, play_intro = True)
        self.playing_bgm = True

    
    def draw(self, drawSurf):
        s = Surface(SCREEN_SIZE, SRCALPHA)
        s.fill((0,0,0,150))
        self.bk.draw(drawSurf)
        self.earth.draw(drawSurf)
        drawSurf.blit(s, vec(0,0))

        super().draw(drawSurf)

    def update(self, seconds):
        if self.text_int == -1:
            self.timer += seconds
            if self.timer >= 1.2:
                self.text_int = 0
                self.timer = 0.0
            else:
                return

        if self.text_int == 0:
            if not self.speaking:
                self.display_text(SPEECH["intro_1"], 1)
                self.text_int += 1

        elif self.text_int == 1:
            if not self.playing_bgm and TM.opening == False:
                self.play_bgm()

            if not self.speaking:
                self.text_int += 1
                return


        elif self.text_int == 2:
            AM.fadeout_bgm(1000)
            self.text_int += 1
            return

        
        elif self.text_int == 3:
            if not AM.bgm_channel.get_busy():
                self.ready_to_transition = True
                self.text_int += 1
            return
        
        elif self.text_int == 4:
            return

        super().update(seconds, play_music = False, update_bgm=False)

class Name(Room):
    def __init__(self):
        super().__init__(bgm="06", vol=20)
        #   Lists of objects in the room    #
        #   Interactable Npcs
        self.npcs = [
        ]
        
        #   Enemies
        self.enemies = [
        ]

        #   Unloaded Enemies
        self.unloaded_enemies = []

        #   Tiles
        self.tiles = []
    
    def play_bgm(self):
        AM.play_ost(self.bgm, volume=20.0, play_drums=False, play_intro = False)
        self.playing_bgm = True

    def draw(self, drawSurf):
        drawSurf.fill((255,255,255))
        super().draw(drawSurf)

    def update(self, seconds):
        super().update(seconds, update_bgm = False)  

        if self.text_int == 0:
            if not self.speaking:
                self.display_text(SPEECH["name_1"], 1)
                self.text_int += 1

        elif self.text_int == 1:
            pass
