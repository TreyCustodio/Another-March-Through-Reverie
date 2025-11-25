import os
from pygame import transform, Surface, Rect, SRCALPHA, font
from globals import SCREEN_SIZE, UPSCALED, SCALE_FACTOR, vec
from objects import Drawable, Black, Fading, Room, Intro, RoomManager, Name,\
    Mid_1, Und_1

from UI import EventManager, AudioManager, Title


EVENT_MANAGER = EventManager.getInstance()
AM = AudioManager.getInstance()
RM = RoomManager()
TITLE = Title()
    


class DisplayManager(object):
    """Factory class for the utility that handles the display
    of objects on the scree initialized in main."""

    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._DM()
        return cls._INSTANCE


    class _DM(object):

        def __init__(self):
            #   States Dictionary   #
            self.states = {
                'fading_out': False, # Black alpha increasing
                'fading_in': False, # Black alpha decreasing
                'title': True,
            }

            #   Array containing priotity objects that need to be displayed  #
            self.display_objects = [None]

            #   Black surface used for fading in/out   #
            self.black = Black()

            #   All-purpose Black Background Image  #
            self.bkg = Surface(UPSCALED)
            self.bkg.fill((0,0,0))

            #   Timers and Counters #
            self.display_int = 0
            self.title_timer = 0.0
            self.title_wait = 0.7
            self.fps = 0.0

            #   Currently loaded room   #
            self.room = None

        def play_sound(self, sound) -> None:
            AM.playSFX(sound)

        def draw(self, drawSurf) -> None:
            #   Draw Background #
            # drawSurf.blit(self.bkg, vec(0,0))
            self.draw_background(drawSurf)


            #   Draw Title  #
            if self.states['title']:
                self.title_routine(drawSurf)
            
            #   Draw Game   #
            elif self.states['in_game']:
                self.draw_game(drawSurf)

            #   Fading  #
            self.draw_black(drawSurf)

            #   FPS #
            self.draw_fps(drawSurf)

            return
        
        def draw_fps(self, drawSurf):
            """Display the fps"""
            fnt = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16)
            img = fnt.render(str(round(self.fps, 2)), False, (255, 255, 255), (0,0,0))
            drawSurf.blit(img, list(map(int, vec(2,2))))
        
        def update_fps(self, fps):
            self.fps = fps

        def draw_object(self, drawSurf, index=0):
            """Draw the object at the specified index in display_objects"""
            drawSurf.blit(self.display_objects[index][0], self.display_objects[index][1])

        def draw_background(self, drawSurf):
            drawSurf.blit(self.bkg, vec(0,0))

        def set_title_menu(self):
            TITLE.initialize()

            #   "Another March Through Reverie" #
            #   Set the font
            fnt = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16)
            delta = 48

            #   Another March (White)
            text_surface = fnt.render('Another March', True, (255, 254, 184))
            self.display_objects[0] = (Fading(text_surface, d_a=2), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, text_surface.get_height() + delta))
            self.display_objects[0][0].fade_in()


            #   Another March (Yellow)
            text_surface = fnt.render('Another March', True, (255, 241, 83))
            self.display_objects.append((Fading(text_surface, d_a=1), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, text_surface.get_height() + delta)))

            #   Through Reverie (White)
            text_surface = fnt.render('Through Reverie', True, (255, 254, 184))
            self.display_objects.append((Fading(text_surface, d_a=4), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, (text_surface.get_height() * 2.5 + delta)) ))

            #   Through Reverie (Yellow)
            text_surface = fnt.render('Through Reverie', True, (241, 255, 83))
            self.display_objects.append((Fading(text_surface, d_a=1), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, (text_surface.get_height() * 2.5 + delta)) ))


            



        def title_routine(self, drawSurf) -> None:
            #   Typical Draw Routine when selecting new/load    #
            if self.display_int == 8:
                if self.title_timer >= self.title_wait:
                    TITLE.draw(drawSurf)
                for i in range(len(self.display_objects)):
                    self.draw_object(drawSurf, i)

                return

            #   Display Opening Credits and make the title appear   #
            if self.display_int == 0:
                self.play_sound("gong.wav")
                fnt = font.Font(os.path.join("UI", "fonts", 'OpenSans-Regular.ttf'), 16)
                text_surface = fnt.render('Yung Trey Games Presents...', True, (255, 50, 20))
                self.display_objects[0] = (Fading(text_surface, d_a=6), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, UPSCALED[1] // 2 - text_surface.get_height() // 2))
                self.display_objects[0][0].set_opaque()
                self.display_int = 1

            if self.display_int == 1 or self.display_int == 2:
                self.draw_object(drawSurf)
            
            if self.display_int == 3:
                drawSurf.fill((0,0,0))
                self.play_sound("gong.wav")
                fnt = font.Font(os.path.join("UI", "fonts", 'OpenSans-Regular.ttf'), 16)
                text_surface = fnt.render('With Yung Trizzy on that Soundtrack...', True, (255, 50, 20))
                self.display_objects[0] = (Fading(text_surface, d_a=6), vec(UPSCALED[0] // 2 - text_surface.get_width() //2, UPSCALED[1] // 2 - text_surface.get_height() // 2))
                self.display_objects[0][0].set_opaque()
                self.display_int = 4

            if self.display_int == 4 or self.display_int == 5:
                self.draw_object(drawSurf)


            #   Draw title logo and Menu Options    #
            if self.display_int == 6:
                self.set_title_menu()
                self.display_int = 7
            
            if self.display_int == 7:
                for i in range(len(self.display_objects)):
                    self.draw_object(drawSurf, i)
                


        
        def draw_game(self, drawSurf) -> None:
            surf = Surface(UPSCALED)
            surf.fill((255,255,255))
            drawSurf.blit(surf, vec(0,0))

            RM.get_current_room().draw(drawSurf)
            

        def draw_black(self, drawSurf):
            drawSurf.blit(self.black, vec(0,0))

        def handle_events(self) -> None:
            """Receive interpretations from the event manager and update the display manager's states accordingly"""
            if self.states['title']:
                #   Selecting Menu Option   #
                if self.display_int == 8 and self.title_timer >= self.title_wait and not(TITLE.start_new or TITLE.load):
                    TITLE.handle_events()

                    #   Transition to game
                    if TITLE.start_new:
                        AM.fadeout_bgm(1500)
                        self.fade_out()

                    elif TITLE.load:
                        AM.fadeout_bgm(1500)
                        self.fade_out()

                #   Title Screen Appearing  #
                if self.display_int < 7:
                    if EVENT_MANAGER.perform_action('interact'):
                        AM.fadeAllSFX(100)
                        self.set_title_menu()
                        self.display_int = 7
                
                elif self.display_int == 7:
                    if EVENT_MANAGER.perform_action('interact'):
                        AM.fadeAllSFX(100)
                        self.display_objects[0][0].set_opaque()
                        self.display_objects[2][0].set_opaque()
                        self.display_int = 8
            
            elif self.states['in_game']:
                RM.get_current_room().handle_events()

            return
            #   Fade Control Testing    #
            if EVENT_MANAGER.perform_action('interact'):
                self.fade_out()
            
            if EVENT_MANAGER.perform_action('attack1'):
                self.fade_in()

        def fade_out(self) -> None:
            self.states['fading_out'] = True
            self.states['fading_in'] = False
            self.black.fade_out()
        
        def fade_in(self) -> None:
            self.states['fading_in'] = True
            self.states['fading_out'] = False
            self.black.fade_in()
        
        def start_new(self):
            """Transition from title screen to a new game"""
            self.states['title'] = False
            self.states['in_game'] = True
            self.display_objects = []
            self.display_int = 0
            TITLE = None

            RM.set_next_room(Intro)
            # RM.set_next_room(Name)

        
        def load_game(self):
            self.states['title'] = False
            self.states['in_game'] = True
            self.display_objects = []
            self.display_int = 0
            TITLE = None
            RM.set_next_room(Und_1)
            # RM.set_next_room(Mid_1)


        def load_next(self, room):
            """Transition from title screen to a new game"""
            RM.set_next_room(room)
            self.fade_in()

        def update(self, seconds) -> None:
            """Update the display based on the current state"""
            if self.states['title']:
                #   Opening Credits #
                if self.display_int == 1 or self.display_int == 4:
                    if not AM.is_busy():
                        self.display_int += 1
                        self.display_objects[0][0].fade_out()

                if self.display_int == 2 or self.display_int == 5:
                    self.display_objects[0][0].update(seconds)
                    if self.display_objects[0][0].transparent:
                        self.display_int += 1
                
                #   Title Logo and Menu options #
                if self.display_int == 7:
                    self.display_objects[0][0].update(seconds)

                    #   Bottom text appears after top
                    if not self.display_objects[2][0].fading_in and self.display_objects[0][0].get_alpha() >= 210:
                        #   Fade in bottom text
                        self.display_objects[2][0].fade_in()
                    
                    if self.display_objects[0][0].opaque and self.display_objects[2][0].opaque:
                        self.display_int = 8
                    else:
                        for o in self.display_objects:
                            o[0].update(seconds)
                        

                if self.display_int == 8:
                    #   Wait a couple of seconds before playing music   #

                    if self.title_timer >= self.title_wait:
                        #   Fade yellow text in and out for a glow effect
                        #   o[1] and o[3] = yellow
                        o = self.display_objects

                        if o[1][0].transparent:
                            o[1][0].fade_in()
                        elif o[1][0].opaque:
                            o[1][0].fade_out()

                        if o[3][0].transparent:
                            o[3][0].fade_in()
                        elif o[3][0].opaque:
                            o[3][0].fade_out()

                        for o in self.display_objects:
                            o[0].update(seconds)
                        
                        TITLE.update(seconds)

                    else:
                        self.title_timer += seconds

            elif self.states['in_game']:
                RM.get_current_room().update(seconds)

                if RM.get_current_room().ready_to_transition and not self.states['fading_out']:
                    self.fade_out()


            if self.states['fading_out'] or self.states['fading_in']:
                self.black.update(seconds)

                if self.black.opaque:
                    # print("Fade out complete")
                    self.states['fading_out'] = False

                    #   Change states based on Fading   #
                    if self.states['title']:
                        #   Switch to intro cutscene / game
                        if self.display_int == 8:
                            if TITLE.start_new:
                                self.start_new()
                                self.fade_in()
                            elif TITLE.load:
                                self.load_game()
                                self.fade_in()

                    elif self.states['in_game']:
                        #   Switch to intro cutscene / game
                        room = RM.get_current_room()
                        if room.ready_to_transition:
                            self.load_next(room.next_room)


                if self.black.transparent:
                    # print("Fade in complete")
                    self.states['fading_in'] = False
            return