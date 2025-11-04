from pygame import Rect, Surface, draw

from .import Drawable


class Interactable(Drawable):
    """Represents an interactable object in the game"""

    def __init__(self, position, file_name = "luigi.png", offset=(0,0)):
        super().__init__(position, file_name, offset)
        self.interaction_rect = Rect(self.position, (self.image.get_width(), self.image.get_height()))

        #   Text data   #
        self.text = "Weegee time."
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
        #   Draw the interaction Rect   #
        surf = Surface((self.interaction_rect.w, self.interaction_rect.h))
        surf.fill((20,120,255))
        drawSurf.blit(surf, self.position - Drawable.CAMERA_OFFSET)

        #   Draw the sprite #
        super().draw(drawSurf)