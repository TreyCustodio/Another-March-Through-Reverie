from os import path

from utils import vec
from .animated import Animated, State
from .drawable import Drawable

class HudManager(object):
    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._HM()
        return cls._INSTANCE

    class _HM(object):

        def __init__(self):
            """Create space for each hud object, but don't instantiate them"""
            self.initialized = False
            self.heart = None

        def init(self):
            if self.initialized:
                return
            self.initialized = True

            self.heart = Animated(vec(0,0), path.join("misc", "heart.png"), offset=(0,0))
            self.heart.add_state("idle", State(path.join("misc", "heart.png"), fps=32, num_frames=57))

            self._objects = [
                self.heart
            ]

        def draw(self, drawSurf):
            drawSurf.blit(self.heart.image, self.heart.position)
            drawSurf.blit(self.heart.image, self.heart.position)

        
        def update(self, seconds):
            for o in self._objects:
                o.update(seconds)