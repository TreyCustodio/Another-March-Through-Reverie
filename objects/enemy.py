from os import path
from . import Animated, State
from UI import AudioManager, SpriteManager
from globals import vec


SM = SpriteManager.getInstance()

class Enemy(Animated):
    def __init__(self, position = vec(0,0), file_name = "", offset = (0,0),
                 enemy=True):
        super().__init__(position, file_name, offset)



class Raven(Enemy):
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, 'raven_b.png', (0,0))
        self.add_state('idle', State(self.file_name, 0, 0, 8, 3))

    # def set_image(self) -> None:
    #     """Set the object's image"""
    #     #   Get the current state's information #
    #     current_state = self.get_current_state()
    #     file_name = current_state.get_file_name()
    #     row = current_state.get_row()

    #     #   Define and Set the image   #
    #     new_image = SM.getSprite(file_name, (self.frame, row), enemy=True)
    #     super().set_image()
    
