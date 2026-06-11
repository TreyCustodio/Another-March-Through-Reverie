from os import path

from pygame import Rect

from . import Animated, State
from globals import vec

class Weapon(Animated):
    def __init__(self, position, file_name,
                 life_time, velocity, damage=1):
        
        super().__init__(position, file_name, offset=(0,0))
        
        #   Physics #
        self.vel = velocity
        self.timer = 0.0
        self.life_time = life_time
        self.damage = damage

        #   States  #
        self.dead = False
    
    def get_collision_rect(self):
        return None
    
    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()
    
    def get_size(self):
        return self.image.get_size()
    
    def get_damage(self):
        if self.dead:
            return 0
        
        return self.damage
    
    def collide(self):
        if self.dead:
            return
        
        self.dead = True

    def update(self, seconds):
        if self.dead:
            return
        
        self.timer += seconds

        if self.timer >= self.life_time:
            self.dead = True
            return
        
        self.position += self.vel * seconds
        super().update(seconds)


class Shot(Weapon):
    def __init__(self, position, direction='right'):
        self.direction = direction
        velocity = vec(400, 0) if direction == 'right' else vec(-400, 0)

        super().__init__(position, file_name=path.join("misc", "shot.png"),
                         life_time=1.0, velocity=velocity, damage=1)

        if direction == "left":
            self.add_state("idle", State(path.join("misc", "shot.png"), row=1, fps=32, num_frames = 6))
        elif direction == "right":
            self.add_state("idle", State(path.join("misc", "shot.png"), row=0, fps=32, num_frames = 6))



    def get_collision_rect(self):
        return Rect(self.position, (self.get_width(), 5))