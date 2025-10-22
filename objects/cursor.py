from . import Drawable
from globals import vec

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