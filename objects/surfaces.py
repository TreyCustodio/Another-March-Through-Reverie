from globals import UPSCALED, vec
from pygame import Surface, SRCALPHA


class Static(Surface):
    def __init__(self, surface):
        super().__init__(UPSCALED, SRCALPHA)
        self.image = surface
        if surface:
            self.blit(surface, vec(0,0))

    def update(self, seconds):
        return
    
class Fading(Surface):
    """A fadeable surface object"""
    def __init__(self, surface = None, d_a = 1, transparent = True):
        """Black surface initialized to transparent"""
        #   Initialize a black surface the size of the screen   #
        super().__init__(UPSCALED, SRCALPHA)
        if surface:
            self.blit(surface, vec(0,0))

        #   State Values    #
        self.fading_out = False # Black alpha increasing
        self.fading_in = False # Black alpha decreasing

        self.opaque = not transparent # Black is fully opaque
        self.transparent = transparent # Black is fully transparent

        #   Transparency Control    #
        if transparent:
            self.alpha = 0
        else:
            self.alpha = 255

        self.d_alpha = d_a
        self.set_alpha(self.alpha)
            
    def set_delta(self, delta):
        """Change the amount which the transparency will increase by every frame"""
        self.d_alpha = delta

    def fade_out(self):
        """Start fading out"""
        self.fading_out = True
        self.fading_in = False

        self.opaque = False
        self.transparent = False

    def fade_in(self):
        """Start fading in"""
        self.fading_in = True
        self.fading_out = False

        self.opaque = False
        self.transparent = False

    def set_opaque(self):
        """Set the black surface to be fully opaque"""
        self.alpha = 255
        self.opaque = True
        self.transparent = False
        self.set_alpha(self.alpha)

    def set_transparent(self):
        """Set the black surface to be fully transparent"""
        self.alpha = 0
        self.transparent = True
        self.opaque = False
        self.set_alpha(self.alpha)


    def update(self, seconds):
        #   Fading In   #
        if self.fading_in:
            self.alpha += self.d_alpha
            if self.alpha >= 255:
                self.set_opaque()
            else:
                self.set_alpha(self.alpha)
        
        #   Fading Out    #
        elif self.fading_out:
            self.alpha -= self.d_alpha
            if self.alpha <= 0:
                self.set_transparent()
            else:
                self.set_alpha(self.alpha)


class Black(Fading):
    def __init__(self):
        super().__init__(d_a=4)
        self.fill((0,0,0,255))

    def update(self, seconds):
        #   Fade Game Out -- Increase Black Alpha   #
        if self.fading_out:
            self.alpha += self.d_alpha
            if self.alpha >= 255:
                self.set_opaque()
            else:
                self.set_alpha(self.alpha)
        
        #   Fade Game In -- Decrease Black Alpha    #
        elif self.fading_in:
            self.alpha -= self.d_alpha
            if self.alpha <= 0:
                self.set_transparent()
            else:
                self.set_alpha(self.alpha)