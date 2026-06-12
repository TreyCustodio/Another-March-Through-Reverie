from pygame import Surface, SRCALPHA

from globals import SCREEN_SIZE
from utils import EventManager, AudioManager

EM = EventManager.getInstance()
AM = AudioManager.getInstance()

class PauseEngine(object):
    """This class is responsible for handling
    how the game operates while the game is paused"""
    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._PE()
        return cls._INSTANCE

    class _PE:
        def __init__(self):
            self.black = Surface(SCREEN_SIZE, flags = SRCALPHA)
            self.black.fill((0,0,0,150))
            return
        
        def draw(self, drawSurf):
            drawSurf.blit(self.black, (0,0))
        
        def handle_events(self):
            return
        
        def update(self, seconds):
            # print("The game is paused")
            return