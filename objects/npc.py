from pygame import Rect, Surface, draw

from random import randint
from .import Drawable, Animated


class Interactable(Drawable):
    """Represents an interactable object in the game"""

    def __init__(self, position, file_name = "luigi.png", offset=(0,0),
                 text = "Weegee time.$$"):
        super().__init__(position, file_name, offset)
        self.interaction_rect = Rect(self.position, (self.image.get_width(), self.image.get_height()))

        #   Text data   #
        self.text = text
        self.box = 0

        #   Animation Data  #
        self.row = 0
        self.frame = 0
        self.animation_timer = 0.0

    def get_interaction_rect(self):
        return Rect(self.position, (self.image.get_width(), self.image.get_height()))

    
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


class Weegee(Interactable):
    def __init__(self, position):
        super().__init__(position, "luigi.png", (0,0), "It's Weegee time.")
        self.text = "Hello Mario.$$Today we will be discussing\nthe male penis and testicles."

    def update(self, seconds):
        return
        r = randint(0,1)
        if r == 0:
            self.text = "It's Weegee time."
        elif r == 1:
            self.text = "Hello Mario.$$\nToday we will be discussing\nthe male penis and testicles."

class RavenNpc(Interactable):
    def __init__(self, position, text = "Sup mah n****"):
        super().__init__(position, file_name="raven_b.png", offset=(0, 0), text=text)