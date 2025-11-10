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
            self.skipping = False
            self.fading = False

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
            self.default_color = (255, 254, 200)
            self.color = (255, 254, 200)
            self.coloring = False
            self.alpha = 255
            self.d_alpha = 12

            #   Animation Data  #
            self.text_frame = 0
            self.chars_per_second = 12
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
            self.shadow.set_color(self.default_color)
            self.shadow.set_position((self.char_pos[0] + self.char_space, self.char_pos[1]))



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
            self.chars_per_second = 12
            self.char_timer = 0.0

        def play_sound(self):
            if self.type == 0:
                name = "text_1.wav"
            elif self.type == 1:
                name = "text_2.wav"

            name = os.path.join("text", name)
            AM.playText(name)

        def draw(self, drawSurf):
            #   Draw the Display Surface / Textbox  #
            print(self.position)
            drawSurf.blit(self.display_surface, self.position)

            #   Draw the "waiting for input" triangle   #
            if self.waiting:
                drawSurf.blit(self.triangle, self.triangle.position)
            
            #   Draw the text index shadow  #
            else:
                if not self.fading:
                    drawSurf.blit(self.shadow, self.position + self.shadow.position)
            
            return
        
        def handle_events(self):
            #   Opening -- do nothing   #
            if self.opening:
                return
            
            if EM.perform_action('space') and not self.closing:
                self.closing = True
                if self.clearing:
                    self.char_pos = vec(0,0)
                    self.set_shadow_position()
                    self.clearing = False
                    self.fading = True
                    self.set_box()

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
                        self.set_shadow_position()
                        self.fading = True
                        self.clearing = False
                        self.set_box()
                    #   Play a sound

            else:
                self.skipping = EM.is_active('interact')
            return
        
        def set_shadow_position(self, width = 1):
            self.shadow.set_image(width, self.color)
            self.shadow.set_position((self.char_pos[0] + self.char_space, self.char_pos[1]))

        def set_box(self):
            #   Need to remove textbox.png from spriteManager's memory  #
            if self.type == 0:
                self.display_surface = SM.getSprite("textbox.png", (self.frame,self.row))
                del SM._surfaces['textbox.png']
                
            elif self.type == 1:
                self.display_surface = Surface(SCREEN_SIZE, SRCALPHA)
            

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
            
            #   buffering
            elif char == "*":
                next_char = self.text[self.char_index + 1]
                #   Take a breath
                if next_char == ",":
                    self.char_timer -= 0.2
                    self.char_index += 1
                
                #   Take a pause
                elif next_char == ".":
                    self.char_timer -= 0.4
                    self.char_index += 1

                else:
                    return True
                
                return False

            #   %c -> Color char
            elif char == "%":
                if self.coloring:
                    self.coloring = False
                    self.color = self.default_color
                    self.shadow.set_color(self.default_color)
                    return

                self.coloring = True
                next_char = self.text[self.char_index + 1]

                if next_char == "g":
                    self.color = (171, 255, 53)

                elif next_char == "r":
                    self.color = (200, 0, 0)

                elif next_char == "w":
                    self.color = (170, 170, 255)
                
                elif next_char == "p":
                    self.color = (255, 28, 122)

                self.shadow.set_color(self.color)
                self.char_index += 1
                return False

            #   && -> Wait for input
            elif char == "&":
                next_char = self.text[self.char_index + 1]
                if next_char == "&":
                    #   Update the state
                    self.waiting = True
                    EM.deactivate('interact')
                    self.triangle.set_position(self.char_pos.copy())


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
                    EM.deactivate('interact')


                    #   Skip both "$$" characters
                    self.char_index += 1

                    #   Do not display "$$"
                    return False
                
            return True

        def display(self, char, play):
            #  Get the images
            char_image = self.font.render(char, False, self.color)
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
            if play and not AM.menu_channel.get_busy():
                self.play_sound()
            
            #  Set the char position
            width = char_image.get_width()

            self.char_pos[0] += width + self.char_space
            self.set_shadow_position(width)
            

        def update(self, seconds):
            #   Open box Animation  #
            if self.opening:
                #   Each frame, upscale the x axis
                self.x_scale += 20
                if self.x_scale >= 480:
                    self.opening = False
                    self.x_scale = 480

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
            
            elif self.fading:
                self.alpha -= self.d_alpha
                if self.alpha <= 0:
                    self.display_surface.set_alpha(0)
                    self.alpha = 255
                    self.chars = []
                    self.set_box()
                    self.fading = False
                else:
                    self.display_surface.set_alpha(self.alpha)
                
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

            if self.skipping:
                ready = self.char_timer >= 1/(self.chars_per_second * 8)
            else:
                ready = self.char_timer >= 1/self.chars_per_second

            if ready:
                #   ----- Reset the timer -----
                self.char_timer = 0.0

                #   ----- Get the next Char -----
                char = self.text[self.char_index]
                play = char != " " and char != "\n"

                #   ----- Parse the next Char -----
                display = self.parse(char)
                self.parsed = True

                #   ----- Display the Char -----
                if display:
                    self.display(char, play)

                #   ----- Increase the index -----
                self.char_index += 1

            #   Check if the dialogue is finished   #
            if self.char_index == len(self.text):
                self.waiting = True
                EM.deactivate('interact')
                self.end = True

                