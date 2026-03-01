import os
from pygame import font, Surface, PixelArray, transform

from globals import UPSCALED, vec
from objects import Static, Fading, Drawable, Cursor
from UI import SpriteManager, EventManager, AudioManager

"""
The code contained in this file defines how
menus such as the title screen are handled.
"""

SM = SpriteManager.getInstance()
EM = EventManager.getInstance()
AM = AudioManager.getInstance()


class Title(object):
    """
    This class functions as the engine for the title screen.
    """
    def __init__(self):
        
        font.init()
        self.initialized = False

        #   Images to draw #
        self.display_objects = []
        self.shadows = []

        #   Menu Options    #
        #   States
        self.start_new = False
        self.load = False

        #   Set the font
        fnt = font.Font(os.path.join("UI", "fonts", 'OpenSans-Regular.ttf'), 16)
        self.fnt = fnt
        self.white = (255, 254, 184)
        self.red = (255, 20, 20)
        # self.shadow_color = (10, 120, 10)
        self.shadow_color = (0,0,0)

        # self.selected_shadow = (60, 60, 10)
        self.selected_shadow = (0,0,0)

        shadow_offset = vec(-1, -1)

        #   New Game
        text_surface = fnt.render("New Game", False, self.white)
        self.display_objects.append([Fading(text_surface, d_a=1, transparent=False), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, UPSCALED[1] // 2 + text_surface.get_height() - 16)])
        
        new_shadow = fnt.render("New Game", False, self.shadow_color)
        self.shadows.append([Static(new_shadow), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, UPSCALED[1] // 2 + text_surface.get_height() - 16) - shadow_offset])
        
        #   Load Game
        text_surface = fnt.render("Load Game", False, self.white)
        self.display_objects.append([Fading(text_surface, d_a=1, transparent=False), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, (UPSCALED[1] // 2 + (text_surface.get_height()) * 2)- 16)])
        
        load_shadow = fnt.render("Load Game", False, self.shadow_color)
        self.shadows.append([Static(load_shadow), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, (UPSCALED[1] // 2 + (text_surface.get_height()) * 2)- 16) - shadow_offset])


        #   Quit Game :(
        text_surface = fnt.render("Quit Game", False, self.white)
        self.display_objects.append([Fading(text_surface, d_a=1, transparent=False), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, (UPSCALED[1] // 2 + (text_surface.get_height()) * 3) - 16)])
       
        quit_shadow = fnt.render("Quit Game", False, self.shadow_color)
        self.shadows.append([Static(quit_shadow), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, (UPSCALED[1] // 2 + (text_surface.get_height()) * 3) - 16) - shadow_offset])

        #   Background Timers   #
        self.bg_timer = 0.0
        self.bg_time = 6.8
        self.ready_to_fade = False

        self.image_int = 0
        

    def initialize(self):
        #   Play the title theme    #
        # AM.play_ost("01", play_intro=True, play_drums = False)
        AM.play_ost("15", play_intro=True, play_drums = False)


        #   Initialize the pointer  #
        self.pointer = Cursor(vec(0,0), "pointer.png")
        self.pointer.scale_image()

        pos = self.display_objects[0][1].copy()
        pos[0] -= (self.pointer.get_width() + 8)
        pos[1] += (self.pointer.get_height() // 2 - 10)
        self.pointer.set_position(pos)

        #   Render New Game as red  #
        #   Re-render the font
        text_surface = self.fnt.render("New Game", False, self.red)
        new_shadow = self.fnt.render("New Game", False, self.selected_shadow)

        #   Update the values in self.display_objects to the new renders
        self.display_objects[0][0] = Fading(text_surface, d_a=1, transparent=False)
        self.shadows[0][0] = new_shadow
        
        #   Initialize the pointer position to 0
        self.pointer_position = 0 # 0 for new game, 1 for load, 2 for quit

        #   Background Images to loop thru
        self.images = [
            Drawable(vec(0,0), "sunset1.png"),
            Drawable(vec(320*2,0), "sunset1.png"),

            Drawable(vec(0,0), "night2.png"),
            Drawable(vec(320*2,0), "night2.png"),

            Drawable(vec(0,0), "night.png"),
            Drawable(vec(320*2,0), "night.png"),

            Drawable(vec(0,0), "middleground.png"),
            Drawable(vec(320*2,0), "middleground.png"),
        ]
        
        # scale the images
        for i in self.images:
            i.image = transform.scale(i.image, (320 * 2, 240))

        self.initialized = True
    
    def set_image(self):
        #   Reset the image positions
        self.images[self.image_int].position = vec(0,0)
        self.images[self.image_int+1].position = vec(320*2,0)
        
        #   Increment the image int
        self.image_int += 2
        self.image_int %= 8

        #   Reset the state
        self.ready_to_fade = False


    def draw(self, drawSurf):
        for s in self.shadows:
            drawSurf.blit(*s)

        for o in self.display_objects:
            drawSurf.blit(*o)
        
        # self.pointer.draw(drawSurf)
    
    def draw_bg(self, drawSurf):
        if self.initialized:
            self.images[self.image_int].draw(drawSurf)
            self.images[self.image_int+1].draw(drawSurf)
            

    def handle_events(self):
        #   Select the Option   #
        if EM.perform_action('interact'):
            #   Start a new game
            if self.pointer_position == 0:
                self.start_new = True

            #   Load a game
            elif self.pointer_position == 1:
                self.load = True

            #   Quit the game
            elif self.pointer_position == 2:
                EM.QUIT()

            else:
                return
            
            #   Play a sound
            

        #   Move Option Down    #
        elif self.pointer_position < 3 and EM.perform_action('motion_down'):
            # AM.playMenuSFX("menu_1.wav")
            # AM.playSFX("menu_1.wav")

            self.pointer_position += 1

            #   Set to Load
            if self.pointer_position == 1:
                pos = self.display_objects[1][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make Load red
                text_surface = self.fnt.render("Load Game", False, self.red)
                self.display_objects[1][0] = Fading(text_surface, d_a=1, transparent=False)
                load_shadow = self.fnt.render("Load Game", False, self.selected_shadow)
                self.shadows[1][0] = load_shadow

                #   Make New White
                text_surface = self.fnt.render("New Game", False, self.white)
                self.display_objects[0][0] = Fading(text_surface, d_a=1, transparent=False)
                new_shadow = self.fnt.render("New Game", False, self.shadow_color)
                self.shadows[0][0] = new_shadow

            #   Set to Quit
            elif self.pointer_position == 2:
                pos = self.display_objects[2][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make Quit red
                text_surface = self.fnt.render("Quit Game", False, self.red)
                self.display_objects[2][0] = Fading(text_surface, d_a=1, transparent=False)
                text_surface = self.fnt.render("Quit Game", False, self.selected_shadow)
                self.shadows[2][0] = text_surface

                #   Make Load white
                text_surface = self.fnt.render("Load Game", False, self.white)
                self.display_objects[1][0] = Fading(text_surface, d_a=1, transparent=False)
                shadow = self.fnt.render("Load Game", False, self.shadow_color)
                self.shadows[1][0] = shadow
            
            #   Wrap back to New
            elif self.pointer_position == 3:
                self.pointer_position = 0
                pos = self.display_objects[0][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make New red
                text_surface = self.fnt.render("New Game", False, self.red)
                self.display_objects[0][0] = Fading(text_surface, d_a=1, transparent=False)
                shadow = self.fnt.render("New Game", False, self.selected_shadow)
                self.shadows[0][0] = shadow

                #   Make Quit white
                text_surface = self.fnt.render("Quit Game", False, self.white)
                self.display_objects[2][0] = Fading(text_surface, d_a=1, transparent=False)
                shadow = self.fnt.render("Quit Game", False, self.shadow_color)
                self.shadows[2][0] = shadow
            
            else:
                return
            
            #   Play menu sound
            AM.play_menu_sfx(os.path.join("menu", "menu_1.wav"))

        #   Move Option Up  #
        elif self.pointer_position >= 0 and EM.perform_action('motion_up'):
            # AM.playMenuSFX("menu_1.wav")
            # AM.playSFX("menu_1.wav")
            self.pointer_position -= 1

            #   Set to Quit
            if self.pointer_position == -1:
                self.pointer_position = 2
                pos = self.display_objects[2][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make Quit Red
                text_surface = self.fnt.render("Quit Game", False, self.red)
                self.display_objects[2][0] = Fading(text_surface, d_a=1, transparent=False)
                text_surface = self.fnt.render("Quit Game", False, self.selected_shadow)
                self.shadows[2][0] = text_surface

                #   Make New White
                text_surface = self.fnt.render("New Game", True, self.white)
                self.display_objects[0][0] = Fading(text_surface, d_a=1, transparent=False)
                new_shadow = self.fnt.render("New Game", False, self.shadow_color)
                self.shadows[0][0] = new_shadow

            #   Set to Load
            elif self.pointer_position == 1:
                pos = self.display_objects[1][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make Load Red
                text_surface = self.fnt.render("Load Game", False, self.red)
                self.display_objects[1][0] = Fading(text_surface, d_a=1, transparent=False)
                shadow = self.fnt.render("Load Game", False, self.selected_shadow)
                self.shadows[1][0] = shadow

                #   Make Quit White
                text_surface = self.fnt.render("Quit Game", False, self.white)
                self.display_objects[2][0] = Fading(text_surface, d_a=1, transparent=False)
                shadow = self.fnt.render("Quit Game", False, self.shadow_color)
                self.shadows[2][0] = shadow

            #   Set to New
            elif self.pointer_position == 0:
                pos = self.display_objects[0][1].copy()
                pos[0] -= (self.pointer.get_width() + 8)
                pos[1] += (self.pointer.get_height() // 2 - 10)
                self.pointer.set_position(pos)

                #   Make New Red
                text_surface = self.fnt.render("New Game", False, self.red)
                self.display_objects[0][0] = Fading(text_surface, d_a=1, transparent=False)
                shadow = self.fnt.render("New Game", False, self.selected_shadow)
                self.shadows[0][0] = shadow
                
                #   Make Load White
                text_surface = self.fnt.render("Load Game", False, self.white)
                self.display_objects[1][0] = Fading(text_surface, d_a=1, transparent=False)
                shadow = self.fnt.render("Load Game", False, self.shadow_color)
                self.shadows[1][0] = shadow
            
            else:
                return
            
            #   Play menu sound
            AM.play_menu_sfx(os.path.join("menu", "menu_1.wav"))

    
    def update_bg(self, seconds):
        if not AM.playing_intro:
            self.images[self.image_int].position[0] -= 1
            self.images[self.image_int + 1].position[0] -= 1
            
            if not self.ready_to_fade:
                if self.images[self.image_int].position[0] <= -(320 * 2 + (80)):
                    self.ready_to_fade = True

    def update(self, seconds):
        for o in self.display_objects:
            o[0].update(seconds)
        
        # self.pointer.update(seconds)
