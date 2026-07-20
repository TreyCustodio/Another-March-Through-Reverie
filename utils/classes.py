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
    def __init__(self, position, file_name, offset, size = vec(16,16), property = 1):
        """Properties:
        0 -> No collision
        1 -> Solid collision
        """
        self.image = SM.getSprite(os.path.join("tiles", file_name), offset)
        self.position = position
        self.size = size
        self.property = property

    def draw(self, drawSurf, draw_rect = False):
        drawSurf.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
        
        if draw_rect:
            surf = pygame.Surface(self.get_collision_rect().size, pygame.SRCALPHA)
            if self.property == 0:
                color = (173, 216, 230, 100)
            else:
                color = (140, 216, 255, 180)
            surf.fill(color)
            drawSurf.blit(surf, list(map(int, self.position - Drawable.CAMERA_OFFSET)))

    def get_collision_rect(self):
        return pygame.Rect(self.position, (self.get_width(), self.get_height()))

class Door(Tile):
    def __init__(self, position, file_name, offset, size=vec(16, 16), property=0,
                 next_room = None, exit_position = vec(0,0)):
        self.next_room = next_room
        self.exit_position = exit_position
        super().__init__(position, file_name, offset, size, property)

    def get_width(self):
        return self.size[0]
    
    def get_height(self):
        return self.size[1]
    
    def get_next_room(self):
        return self.next_room
    
    def set_next_room(self, room):
        self.next_room = room

    def set_exit_position(self, pos):
        self.exit_position = pos

    def get_exit_position(self):
        return self.exit_position