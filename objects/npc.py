from pygame import Rect, draw

from .import Drawable


class Interactable(Drawable):
    """Represents an interactable object in the game"""

    def __init__(self, position, file_name = "luigi.png", offset=(0,0)):
        super().__init__(position, file_name, offset)
        self.interaction_rect = Rect(self.position, (self.image.get_width(), self.image.get_height()))

        #   Text data   #
        self.text = "Fuck off"
        self.box = 1

        #   Animation Data  #
        self.row = 0
        self.frame = 0
        self.animation_timer = 0.0

    def get_interaction_rect(self):
        return self.interaction_rect
    
    def get_box(self):
        return self.box
    
    def get_text(self):
        return self.text
    
    def draw(self, drawSurf):
        #   Draw the sprite #
        super().draw(drawSurf)

        #   Draw the interaction rect   #
        draw.rect(drawSurf, (20,120,255), self.interaction_rect, width=1)