from os import path
from . import Animated, State
from UI import AudioManager, SpriteManager
from globals import vec


SM = SpriteManager.getInstance()

class Enemy(Animated):
    def __init__(self, position = vec(0,0), file_name = "", offset = (0,0),
                 starting_vel = vec(0,0),
                 movement_frames = 16):
        
        super().__init__(position, file_name, offset)

        self.movement_counter = 0
        self.movement_frames = movement_frames
        self.vel = starting_vel


class Raven(Enemy):
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, 'raven_b.png', (0,0),
                         starting_vel=vec(32, 0), movement_frames=64)
        self.add_state('idle', State(self.file_name, 0, 0, 8, 3))
        self.add_state('left', State(self.file_name, 0, 0, 8, 3))
        self.add_state('right', State(self.file_name, 0, 1, 8, 3))

        self.set_state("right")


    def update(self, seconds):
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
    
