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
        
        offset = vec(objPos[0], objPos[1]) + (objSize // 2) - (SCREEN_SIZE // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - SCREEN_SIZE[i])))
        
        cls.CAMERA_OFFSET = offset

    @classmethod
    def updateOffsetPos(cls, position, worldSize):
        """Update the camera to focus on a position within a given world size"""
        objPos = position
        
        offset = objPos - (SCREEN_SIZE // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - SCREEN_SIZE[i])))
        
        cls.CAMERA_OFFSET = offset

    def __init__(self, position=vec(0,0), file_name="null.png", offset=None,
                 enemy=False):
        self.position = position
        self.image = SM.getSprite(fileName=file_name, offset=offset, enemy=enemy)
    
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

    #   Abstract Method #
    def update(self, seconds):
        return
    

class StaticImage(Drawable):
    def __init__(self, position, image):
        self.position = position
        self.image = image


class GlowingBox(object):
    def __init__(self, position=vec(0,0), size=vec(16,16),
                 margin_x = 16, margin_y = 16,
                 color = (142, 142, 255), delta = 60,
                 change_r = True, change_g = True, change_b = False,
                 glows_per_second = 16, brightening = True):
        
        #   Positional Data #
        self.position = position
        self.size = size

        #   Animation Data  #
        self.color = color
        self.delta = delta
        self.counter = 0
        self.glow_timer = 0.0
        self.glows_per_second = glows_per_second
        self.brightening = brightening
        self.change_r = change_r
        self.change_g = change_g
        self.change_b = change_b
        self.alpha = 255
        self.d_alpha = 6

        #   Surface to draw on  #
        self.surf = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        #   Rects to draw   #
        self.rect = pygame.Rect(margin_x, margin_y, *size)
        self.border1 = pygame.Rect(margin_x - 1, margin_y - 1, size[0] + 2, size[1] + 2)
        self.border2 = pygame.Rect(margin_x - 2, margin_y - 2, size[0] + 4, size[1] + 4)

        #   Additional States   #
        self.closing = False
        self.closed = False
        self.opening = True
        self.opened = False

        self.open()

    def init(self, brighten = True,
             change_r = True, change_g = True, change_b = False):
        """Reinitialize an existing box"""
        self.closed = False
        self.alpha = 255
        self.brightening = brighten
        self.change_r = change_r
        self.change_g = change_g
        self.change_b = change_b
        self.counter = 0
        self.glow_timer = 0.0

        

    def draw(self, drawSurf):
        pygame.draw.rect(self.surf, (0,0,0), self.border2)
        pygame.draw.rect(self.surf, (255,255,255), self.border1)
        pygame.draw.rect(self.surf, self.color, self.rect)

        drawSurf.blit(self.surf, self.position)

    def open(self):
        self.opening = True
        self.alpha = 0
        self.surf.set_alpha(0)

    def close(self):
        self.closing = True

    def brighten(self):
        r = self.color[0]
        g = self.color[1]
        b = self.color[2]

        if self.change_r:
            r +=1
            r = min(255, r)
        
        if self.change_g:
            g += 1
            g = min(255, g)

        if self.change_b:
            b += 1
            b = min(255, b)

        self.color = (r,g,b)
        self.counter += 1
        if self.counter == self.delta:
            self.brightening = False
            self.counter = 0
    
    def dim(self):
        r = self.color[0]
        g = self.color[1]
        b = self.color[2]

        if self.change_r:
            r -=1
            r = max(0, r)
        
        if self.change_g:
            g -= 1
            g = max(0, g)

        if self.change_b:
            b -= 1
            b = max(0, b)

        self.color = (r,g,b)
        self.counter += 1
        if self.counter == self.delta:
            self.brightening = True
            self.counter = 0
    
    def update(self, seconds):
        self.glow_timer += seconds
        if self.glow_timer >= 1/self.glows_per_second:
            self.glow_timer = 0.0
            if self.brightening:
                self.brighten()
            else:
                self.dim()

        if self.closing:
            self.alpha -= self.d_alpha
            if self.alpha <= 0:
                self.alpha = 0
                self.closed = True
                self.closing = False
            self.surf.set_alpha(self.alpha)
        
        elif self.opening:
            self.alpha += self.d_alpha
            if self.alpha >= 255:
                self.alpha = 255
                self.opened = True
                self.opening = False
            self.surf.set_alpha(self.alpha)