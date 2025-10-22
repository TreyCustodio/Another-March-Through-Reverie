from pygame import Surface, font, SRCALPHA, transform
import os

from . import Player, Drawable
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
           

            #   Animation Data  #
            self.text_frame = 0
            self.chars_per_second = 16
            self.char_timer = 0.0
            self.frames_per_second = 4
            self.animation_timer = 0.0
            self.frame = 0
            self.row = 0
            self.num_frames = 3

        def init(self, text: str, flag: int,
                 fnt = os.path.join("UI", "fonts", 'OpenSans-Regular.ttf'), size=16) -> None:
            """Prepare to display the current dialogue.
            text -> the text to display
            flag -> the type of display
            fnt -> the path to the font
            """
            fnt = os.path.join("UI", "fonts", 'ReturnofGanon.ttf')
            self.text = text
            self.type = flag
            self.font = font.Font(fnt, size)
            self.set_box()

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
            self.closing = False
            self.finished = False

        def reset_metadata(self):
            self.text = ""
            self.type = 0
            self.display_surface = None
            self.font = None

        def set_display(self):
            """Set display parameters to there default settings"""
            self.text_offset = vec(24,16)
            self.char_pos = vec(0,0)
            self.char_space = 4
            self.line_space = 16
            self.char_index = 0

        def reset_animation(self):
            self.text_frame = 0
            self.chars_per_second = 16
            self.char_timer = 0.0

        def play_sound(self, name):
            name = os.path.join("text", name)
            AM.playSFX(name)

        def draw(self, drawSurf):
            x = UPSCALED[0] // 2 - self.display_surface.get_width() // 2
            y = UPSCALED[1] // 2 - self.display_surface.get_height() // 2

            drawSurf.blit(self.display_surface, vec(x,y))
            return
        
        def handle_events(self):
            #   Waiting for input   #
            if self.waiting:
                if EM.perform_action('interact'):
                    #   Update the state
                    self.waiting = False
                    
                    #   Close the box
                    if self.closing:
                        self.finished = True
                        self.set_box()

                    #   Clear the box if needed
                    if self.clearing:
                        self.char_pos = vec(0,0)
                        self.clearing = False
                        self.set_box()
                    #   Play a sound
            return
        
        def set_box(self):
            #   Need to remove textbox.png from spriteManager's memory  #
            self.display_surface = SM.getSprite("textbox.png", (self.frame,0))
            del SM._surfaces['textbox.png']

            # self.display_surface = self.scale(self.display_surface, 2)

            # for c in self.chars:
            #     self.display_surface.blit(c[0], c[1])

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
            char_image = self.font.render(char, False, (255, 254, 184))
            char_shadow = self.font.render(char, False, (0,0,0))
            # white_shadow = self.font.render(char, False, (30, 75, 50))
            # white_shadow = self.font.render(char, False, (255 - 190, 254 - 190, 184 - 150))
            white_shadow = self.font.render(char, False, (0,0,0))


            
            #   Scale the images
            # char_image = self.scale(char_image, 2)
            # char_shadow = self.scale(char_shadow, 2)
            # white_shadow = self.scale(white_shadow, 2)

            #   Define the shadow offsets
            shadow_offset = vec(-2,-2)
            shadow_offset2 = vec(2,2)
            shadow_offset3 = vec(2,-2)
            shadow_offset4 = vec(-2,2)

            white_offset = vec(-1,-1)
            white_offset2 = vec(1,1)
            white_offset3 = vec(1,-1)
            white_offset4 = vec(-1,1)

            #  Blit the image
            ##  Black Shadow
            # self.display_surface.blit(char_shadow, self.char_pos + self.text_offset + shadow_offset)
            # self.display_surface.blit(char_shadow, self.char_pos + self.text_offset + shadow_offset2)
            # self.display_surface.blit(char_shadow, self.char_pos + self.text_offset + shadow_offset3)
            # self.display_surface.blit(char_shadow, self.char_pos + self.text_offset + shadow_offset4)
            
            ##  White Shadow
            # self.display_surface.blit(white_shadow, self.char_pos + self.text_offset + white_offset)
            # self.display_surface.blit(white_shadow, self.char_pos + self.text_offset + white_offset2)
            # self.display_surface.blit(white_shadow, self.char_pos + self.text_offset + white_offset3)
            # self.display_surface.blit(white_shadow, self.char_pos + self.text_offset + white_offset4)
            
            # ##  Actual char
            self.display_surface.blit(char_image, self.char_pos + self.text_offset)
            # self.chars.append([char_image, self.char_pos.copy() + self.text_offset])

            #  Play a sound
            self.play_sound("text_1.wav")
            
            #  Set the char position
            self.char_pos[0] += char_image.get_width() + self.char_space

            

        def update(self, seconds):
            #   Animate the box  #
            # self.animation_timer += seconds
            # if self.animation_timer >= 1/self.frames_per_second:
            #     self.frame += 1
            #     self.frame %= self.num_frames
            #     self.set_box()
            #     self.animation_timer = 0.0

            #   Wait for input  #
            if self.waiting or self.finished:
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
                self.closing = True