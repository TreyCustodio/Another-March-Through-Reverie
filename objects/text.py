from pygame import Surface, font, SRCALPHA, transform
import os

from . import Player, Drawable, Triangle, TextShadow
from globals import SCREEN_SIZE, UPSCALED, SCALE_FACTOR, vec
from UI import SpriteManager, AudioManager, EventManager

#   UI Managers #
SM = SpriteManager.getInstance()
AM = AudioManager.getInstance()
EM = EventManager.getInstance()


class TextManager(object):
    """Manages dialogue in the game"""
    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._TM()
        return cls._INSTANCE

    class _TM(object):
        def __init__(self):
            #   Metadata    #
            self.text = ""
            self.type = 0
            self.display_surface = None
            self.font = None

            #   States  #
            self.opening = False
            self.waiting = False
            self.clearing = False
            self.end = False
            self.closing = False
            self.finished = False

            #   Display Helpers #
            self.text_offset = None
            self.char_pos = None
            self.char_space = None
            self.line_space = None
            self.char_index = None
            self.chars = []
            self.set_display()
            self.position = None
            self.x_scale = 1

            #   Animation Data  #
            self.text_frame = 0
            self.chars_per_second = 16
            self.char_timer = 0.0
            self.frames_per_second = 2
            self.animation_timer = 0.0
            self.frame = 0
            self.row = 0
            self.num_frames = 3

            #   Other display Images    #
            self.triangle = None
            self.shadow = None

        def init(self, text: str, flag: int,
                 fnt = os.path.join("UI", "fonts", 'OpenSans-Regular.ttf'), size=24,
                 row=0
                 ) -> None:
            """Prepare to display the current dialogue.
            text -> the text to display
            flag -> the type of display
            fnt -> the path to the font
            """
            self.opening = True
            self.row = row
            fnt = os.path.join("UI", "fonts", 'ReturnofGanon.ttf')
            size = 16
            self.text = text
            self.type = flag
            self.font = font.Font(fnt, size)
            self.set_box()
            self.triangle = Triangle()
            self.shadow = TextShadow()


        def is_finished(self) -> bool:
            return self.finished
        
        def scale(self, surface, factor) -> Surface:
            w,h = surface.get_size()
            return transform.scale(surface, (w*factor, h*factor))
        
        def reset(self):
            """Reset state and prepare for next dialogue"""
            self.reset_states()
            self.reset_metadata()
            self.set_display()
            self.reset_animation()
            
        def reset_states(self):
            self.opening = False
            self.waiting = False
            self.clearing = False
            self.end = False
            self.closing = False
            self.finished = False

        def reset_metadata(self):
            self.text = ""
            self.type = 0
            self.display_surface = None
            self.font = None

        def set_display(self):
            """Set display parameters to there default settings"""
            self.text_offset = vec(24,12)
            self.char_pos = vec(0,0)
            self.char_space = 0
            self.line_space = 32
            self.char_index = 0
            self.chars = []

        def reset_animation(self):
            self.text_frame = 0
            self.chars_per_second = 16
            self.char_timer = 0.0

        def play_sound(self, name):
            name = os.path.join("text", name)
            AM.playSFX(name)

        def draw(self, drawSurf):
            drawSurf.blit(self.display_surface, self.position)

            if self.waiting:
                drawSurf.blit(self.triangle, self.triangle.position)
            
            else:
                drawSurf.blit(self.shadow, self.position + self.shadow.position)
            return
        
        def handle_events(self):
            #   Opening -- do nothing   #
            if self.opening:
                return
            
            #   Waiting for input   #
            if self.waiting:
                if EM.perform_action('interact'):
                    #   Update the state
                    self.waiting = False
                    
                    #   Close the box
                    if self.end:
                        self.closing = True

                    #   Clear the box if needed
                    if self.clearing:
                        self.char_pos = vec(0,0)
                        self.clearing = False
                        self.chars = []
                        self.set_box()
                    #   Play a sound
            return
        
        def set_box(self):
            #   Need to remove textbox.png from spriteManager's memory  #
            self.display_surface = SM.getSprite("textbox.png", (self.frame,self.row))
            del SM._surfaces['textbox.png']

            if self.opening or self.closing:
                self.display_surface = transform.scale(self.display_surface, (self.x_scale, 96))
            else:
                for c in self.chars:
                    self.display_surface.blit(c[0], c[1])

            

        def parse(self, char):
            #  \n -> Proceed to next line
            if char == "\n":
                self.char_pos[1] += self.line_space
                self.char_pos[0] = 0
                return False
            
            #   && -> Wait for input
            elif char == "&":
                next_char = self.text[self.char_index + 1]
                if next_char == "&":
                    #   Update the state
                    self.waiting = True

                    #   Skip both "&&" characters
                    self.char_index += 1

                    #   Do not display "&&"
                    return False
            
            #   $$ -> Wait for input and clear the box
            elif char == "$":
                next_char = self.text[self.char_index + 1]
                if next_char == "$":
                    #   Update the state
                    self.waiting = True
                    self.clearing = True

                    #   Skip both "$$" characters
                    self.char_index += 1

                    #   Do not display "$$"
                    return False
                
            return True

        def display(self, char):
            #  Get the images
            char_image = self.font.render(char, False, (255, 254, 200))
            shadow1 = self.font.render(char, False, (0,0,0))
            shadow2 = self.font.render(char, False, (0,0,0))

            #   Define the shadow offsets
            shadow_offset = vec(-1,0)
            shadow_offset2 = vec(1,0)
            shadow_offset3 = vec(0,-1)
            shadow_offset4 = vec(0,1)


            #  Blit the image
            self.display_surface.blit(shadow1, self.char_pos + self.text_offset + shadow_offset)
            self.display_surface.blit(shadow2, self.char_pos + self.text_offset + shadow_offset2)
            self.display_surface.blit(shadow1, self.char_pos + self.text_offset + shadow_offset3)
            self.display_surface.blit(shadow1, self.char_pos + self.text_offset + shadow_offset4)
            self.display_surface.blit(char_image, self.char_pos + self.text_offset)

            
            self.chars.append([shadow1, self.char_pos.copy() + self.text_offset + shadow_offset])
            self.chars.append([shadow2, self.char_pos.copy() + self.text_offset + shadow_offset2])
            self.chars.append([shadow1, self.char_pos.copy() + self.text_offset + shadow_offset3])
            self.chars.append([shadow1, self.char_pos.copy() + self.text_offset + shadow_offset4])
            self.chars.append([char_image, self.char_pos.copy() + self.text_offset])


            #  Play a sound
            self.play_sound("text_1.wav")
            
            #  Set the char position
            self.char_pos[0] += char_image.get_width() + self.char_space
            self.shadow.set_position((self.char_pos[0] + self.char_space, self.char_pos[1]))

            

        def update(self, seconds):
            #   Open box Animation  #
            if self.opening:
                #   Each frame, upscale the x axis
                self.x_scale += 20
                if self.x_scale >= 480:
                    self.opening = False
                    self.x_scale = 480
                    self.triangle.set_position(vec(self.position[0] + self.display_surface.get_width() // 2 - self.triangle.get_width() // 2, self.position[1] + self.display_surface.get_height() - self.triangle.get_height()))

                self.set_box()
                x = UPSCALED[0] // 2 - self.display_surface.get_width() // 2
                y = 32
                self.position = vec(x,y)
                return
            
            #   Closing box Animation   #
            elif self.closing:
                #   Each frame, upscale the x axis
                self.x_scale -= 30
                if self.x_scale <= 1:
                    self.opening = False
                    self.x_scale = 1
                    self.finished = True
                self.set_box()
                x = UPSCALED[0] // 2 - self.display_surface.get_width() // 2
                y = 32
                self.position = vec(x,y)
                return
            
            #   Animate the box  #
            self.animation_timer += seconds
            if self.animation_timer >= 1/self.frames_per_second:
                self.frame += 1
                self.frame %= self.num_frames
                self.set_box()
                self.animation_timer = 0.0

            #   Wait for input  #
            if self.waiting or self.finished:
                self.triangle.update(seconds)
                return
            
            #   Display a char every 1/(chars per second) #
            self.char_timer += seconds
            if self.char_timer >= 1/self.chars_per_second:
                #   ----- Get the next Char -----
                char = self.text[self.char_index]

                #   ----- Parse the next Char -----
                display = self.parse(char)

                #   ----- Display the Char -----
                if display:
                    self.display(char)

                #   Reset the timer, increase the index
                self.char_timer = 0.0
                self.char_index += 1

            #   Check if the dialogue is finished   #
            if self.char_index == len(self.text):
                self.waiting = True
                self.end = True

                