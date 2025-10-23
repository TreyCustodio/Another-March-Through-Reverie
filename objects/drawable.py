import os
import pygame
from globals import vec, UPSCALED, SCREEN_SIZE
from UI import SpriteManager

SM = SpriteManager.getInstance()

class Drawable(object):
    CAMERA_OFFSET = vec(0,0)
    
    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        """Update the camera to focus on a trackingObject within a given world size"""
        objSize = trackingObject.get_size()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (SCREEN_SIZE // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - SCREEN_SIZE[i])))
        
        cls.CAMERA_OFFSET = offset

    def __init__(self, position=vec(0,0), file_name="null.png", offset=None):
        self.position = position
        self.image = SM.getSprite(fileName=file_name, offset=offset)
    
    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()
    
    def get_size(self):
        return vec(*self.image.get_size())
    
    def set_position(self, new_position):
        self.position = new_position

    def set_image(self, new_image: pygame.Surface):
        self.image = new_image

    def draw(self, drawSurf):
        drawSurf.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
    
    def scale_image(self, factor=2):
        if factor == 2:
            self.image = pygame.transform.scale2x(self.image)
        else:
            self.image = pygame.transform.scale(self.image, factor)

class StaticImage(Drawable):
    def __init__(self, position, image):
        self.position = position
        self.image = image