from os import path

from pygame import Rect, PixelArray

from . import Animated, State
from UI import AudioManager, SpriteManager
from globals import vec


SM = SpriteManager.getInstance()

class Enemy(Animated):
    def __init__(self, position = vec(0,0), file_name = "", offset = (0,0),
                 starting_vel = vec(0,0), hp = 5, max_hp = 5,
                 movement_frames = 16):
        
        super().__init__(position, file_name, offset)

        self.movement_counter = 0
        self.movement_frames = movement_frames
        self.vel = starting_vel
        self.dead = False
        self.vulnerable = True
        self.vulnerability_timer = 0.0
        self.vulnerability_duration = 0.1

        self.hp = hp
        self.max_hp = max_hp
    
    def get_damage(self):
        return 1
    
    def get_collision_rect(self):
        return Rect(self.position, self.image.get_size())

    def damage(self, weapon):
        if self.vulnerable:
            self.hp -= weapon.get_damage()

            if self.hp <= 0:
                self.dead = True
            else:
                self.vulnerable = False
    
    def update(self, seconds):
        if not self.vulnerable:
            self.vulnerability_timer += seconds
            if self.vulnerability_timer >= self.vulnerability_duration:
                self.vulnerability_timer = 0.0
                self.vulnerable = True
        
        super().update(seconds)

class Raven(Enemy):
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, 'raven_b.png', (0,0),
                         starting_vel=vec(32, 0), movement_frames=64)
        self.add_state('idle', State(self.file_name, 0, 0, 8, 3))
        self.add_state('left', State(self.file_name, 0, 0, 8, 3))
        self.add_state('right', State(self.file_name, 0, 1, 8, 3))
        self.set_state("right")

    
    def draw(self, drawSurf):
        #   Make the sprite red if damaged
        if not self.vulnerable:
            #   Get the pixel array
            arr = PixelArray(self.image)

            #   Replace the colors
            arr.replace((58, 55, 57), (255, 46, 46))
            arr.replace((58, 55, 87), (255, 46, 46))
            arr.replace((251, 242, 54), (255, 46, 46))
            arr.replace((92, 87, 137), (255, 89, 89))
            arr.replace((255, 249, 129), (255, 89, 89))
            arr.replace((34, 32, 52), (148, 10, 10))
            arr.replace((28, 26, 46), (111, 11, 11))




            #   Close the array
            arr.close()

        super().draw(drawSurf)

    def update(self, seconds):
        if self.dead:
            return
        
        if self.movement_counter == self.movement_frames:
            self.vel[0] *= -1
            self.movement_counter = 0
            if self.state == "left":
                self.set_state("right")

            elif self.state == "right":
                self.set_state("left")

        else:
            self.movement_counter += 1
        
        self.position += self.vel * seconds

        super().update(seconds)

    
