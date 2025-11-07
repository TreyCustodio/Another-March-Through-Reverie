from pygame import Surface, SRCALPHA

from . import Drawable
from UI import SpriteManager
from globals import vec

"""
This file defines how objects like cursors and icons function in the game.
These objects are useful in conveying the state of the game to the player.
For example, cursors indicate a selected option, and triangles indicate that the game is waiting for input.
"""

SM = SpriteManager.getInstance()

class Triangle(Surface):
    def __init__(self, position = vec(0,0), d_y = 4):
        """Set an initial position.
        Then move the cursor up and down, updating its y position.
        d_y -> the amount of change in y position before the triangle transitions to moving down/up"""
        
        #   Initialize a surface    #
        super().__init__((32, 16), SRCALPHA)

        #   Define Positional data #
        self.position = position
        self.d_y = d_y
        self.max_y = self.position[1] + d_y
        self.min_y = self.position[1] - d_y

        #   Define Animation data   #
        self.fps = 64
        self.animation_timer = 0.0

        #   Blit the actual sprite on the surface   #
        self.blit(SM.getSprite("triangle.png"), (0,0))

        #   Define Movement States #
        self.moving_up = False
        self.moving_down = True

    def set_position(self, new_position):
        """Update the triangle's positional data to support a new position"""
        self.position = new_position
        self.max_y = new_position[1] + self.d_y
        self.min_y = new_position[1] - self.d_y

    def update(self, seconds):
        """Move the triangle up and down"""
        self.animation_timer += seconds

        if self.animation_timer >= 1/self.fps:
            self.animation_timer = 0.0
            if self.moving_down:
                self.position[1] += 1
                if self.position[1] >= self.max_y:
                    self.moving_down = False
                    self.moving_up = True

            elif self.moving_up:
                self.position[1] -= 1
                if self.position[1] <= self.min_y:
                    self.moving_up = False
                    self.moving_down = True
            
        


class TextShadow(Surface):
    def __init__(self, position = vec(0,0), d_y = 4):
        """Set an initial position.
        Then move the cursor up and down, updating its y position.
        d_y -> the amount of change in y position before the triangle transitions to moving down/up"""
        
        #   Initialize a surface    #
        super().__init__((16,16), SRCALPHA)

        #   Define Animation data   #
        self.position = position

        #   Blit the actual sprite on the surface   #
        self.blit(SM.getSprite("text_circle.png", (1,0)), (0,0))

    
    def set_position(self, position):
        self.position = vec(position[0], position[1] + 16)

class Cursor(Drawable):
    """A drawable object that moves back and forth"""
    def __init__(self, position=vec(0,0), file_name="", offset=None, d_x = 1, max_x = 8):
        super().__init__(position, file_name, offset)

        #   Movement Specs  #
        self.d_x = d_x
        self.max_x = max_x
        self.center_pos = self.position.copy()

        #   States  #
        self.moving_right = True
        self.moving_left = False

    def set_position(self, new_position):
        super().set_position(new_position)
        self.center_pos = new_position.copy()
        self.move_right()
    
    def move_right(self):
        self.moving_right = True
        self.moving_left = False
    
    def move_left(self):
        self.moving_right = False
        self.moving_left = True

    def update(self, seconds):
        """Move the cursor"""
        if self.moving_right:
            self.position[0] += self.d_x
            if self.position[0] >= self.center_pos[0] + self.max_x:
                self.move_left()
        
        elif self.moving_left:
            self.position[0] -= self.d_x
            if self.position[0] <= self.center_pos[0] - self.max_x:
                self.move_right()