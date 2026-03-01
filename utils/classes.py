import os

import pygame

from UI import SpriteManager, AudioManager, EventManager
from objects import Drawable
from globals import vec

"""
This file contains helper classes and objects
that will be used to construct rooms.
"""

SM = SpriteManager.getInstance()
EM = EventManager.getInstance()
AM = AudioManager.getInstance()

class Tile(Drawable):
    """Basic tile. No Collsion"""
    def __init__(self, position, file_name, offset, size = vec(16,16), property = 0):
        self.image = SM.getSprite(os.path.join("tiles", file_name), offset)
        self.position = position
        self.size = size
        self.property = property

    def draw(self, drawSurf, draw_rect = False):
        drawSurf.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
        if draw_rect:
            surf = pygame.Surface(self.size, pygame.SRCALPHA)
            surf.fill((173, 216, 230,100))
            drawSurf.blit(surf, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
