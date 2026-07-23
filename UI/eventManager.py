from pygame import event, joystick
from pygame.locals import *

class EventManager(object):
    """Factory class used to call the singleton Event Manager Class,
    which interprets all input from the user and tells the engine what the user is doing."""

    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._EM()
        return cls._INSTANCE
    
    class _EM(object):
        """Monitors input from the user and passes the interpretation to the engine"""

        def __init__(self):
            #   Dictionary of actions and whether or not they are active/inactive (0 or 1)  #
            self.actions = {
                #   Auxillary Commands
                'pause': False,

                #   Action Commands
                'interact': False,
                'attack1': False, # shooting
                'attack2': False, # boosting
                'special': False,
                'evasive': False,
                'space': False,

                #   Movement (Arrow keys, WASD, Controller Analog stick)
                'motion_down': False,
                'motion_left': False,
                'motion_up': False,
                'motion_right': False,

                #   Mouse Motion
            }
            
            #   Joysticks
            self.joysticks = []

            #   Quit Boolean
            self.quit = False
            
            #   Analog stick deadzone
            self.deadzone = 0.2
            self.down_deadzone = 0.8
            self.up_deadzone = 0.8
            self.axis_left_active = False
            self.axis_right_active = False
            self.axis_up_active = False
            self.axis_down_active = False

            #   Buffer data
            self.buffing = False
            self.buffer_timer = 0.0
            self.buff_time = 0.5
        
        def init(self):
            """Prepare for takeoff!!"""
            #   Initialize any joysticks    #
            joystick_count = joystick.get_count()
            for i in range(joystick_count):
                try:
                    joy = joystick.Joystick(i)
                    joy.init()
                    self.joysticks.append(joy)
                    print(f"Initialized joystick {i}: {joy.get_name()}")
                except:
                    print(f"Unable to connect Joystick {i}")

        def QUIT(self):
            self.quit = True

        def activate(self, action):
            if action in self.actions:
                self.actions[action] = True
        
        def deactivate(self, action):
            if action in self.actions:
                self.actions[action] = False

        def is_buffing(self) -> bool:
            """Return True if buffering"""
            return self.buffing
        
        def is_active(self, action) -> None:
            """Check if an action is active"""
            if action in self.actions:
                return self.actions[action]
            return False
        
        def perform_action(self, action) -> None:
            """Check if an action is active and turn it off afterward"""
            if action in self.actions:
                if self.actions[action]:
                    self.actions[action] = False
                    return True
            return False
        
        def deactivate_all(self) -> None:
            """Deactivate all actions"""
            for action in self.actions:
                self.actions[action] = False

        def buffer_input(self, buff_time = 0.2) -> None:
            """Buffer the input"""
            self.buffing = True
            self.buff_time = buff_time
            return
        
        def update_buffer(self, seconds) -> None:
            """Update the buffer value for certain inputs such as moving through menus"""
            self.buffer_timer += seconds
            if self.buffer_timer >= self.buff_time:
                self.buffing = False
                self.buffer_timer = 0.0

        def main(self, print_events = False) -> bool:
            """Get events from the pygame event queue and interpret them.
            Return True to continue the game.
            Return False to quit the game."""
            if self.quit:
                return False
            
            for ev in event.get():
                if print_events:
                    print(ev, end="\n\n")

                #   Check for High-priority events
                if ev.type == QUIT:
                    return False
                
                elif ev.type == JOYDEVICEADDED:
                    # joystick_count = joystick.get_count()
                    # for i in range(len(self.joysticks) - 1, joystick_count):
                    #     joy = joystick.Joystick(i)
                    #     joy.init()
                    #     self.joysticks.append(joy)
                    #     print(f"Initialized joystick {i}: {joy.get_name()}")
                    return True
                
                elif ev.type == JOYDEVICEREMOVED:
                    print(f"Joystick {ev.instance_id} disconnected")
                    self.deactivate_all()
                    return True

                #   Keyboard Controls   #
                #   Keys Down
                elif ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        return False
                    
                    elif ev.key == K_RETURN:
                        self.activate('pause')

                    elif ev.key == K_z:
                        self.activate('interact')
                    
                    elif ev.key == K_x:
                        self.activate('attack1')
                        self.activate('attack2')


                    elif ev.key == K_v:
                        self.activate('evasive')

                    elif ev.key == K_LEFT:
                        self.activate('motion_left')
                    
                    elif ev.key == K_RIGHT:
                        self.activate('motion_right')

                    elif ev.key == K_UP:
                        self.activate('motion_up')

                    elif ev.key == K_DOWN:
                        self.activate('motion_down')

                    elif ev.key == K_SPACE:
                        self.activate('space')

                #   Keys Up
                elif ev.type == KEYUP:
                    if ev.key == K_RETURN:
                        self.deactivate('pause')

                    elif ev.key == K_z:
                        self.deactivate('interact')
                    
                    elif ev.key == K_x:
                        self.deactivate('attack1')
                        self.deactivate('attack2')
                        

                    elif ev.key == K_LEFT:
                        self.deactivate('motion_left')
                    
                    elif ev.key == K_RIGHT:
                        self.deactivate('motion_right')

                    elif ev.key == K_UP:
                        self.deactivate('motion_up')

                    elif ev.key == K_DOWN:
                        self.deactivate('motion_down')
                    
                    elif ev.key == K_SPACE:
                        self.deactivate('space')
                    
                    elif ev.key == K_v:
                        self.deactivate('evasive')


                #   Mouse Controls  #
                elif ev.type == MOUSEMOTION:
                    pass
                
                elif ev.type == MOUSEBUTTONDOWN:
                    pass

                elif ev.type == MOUSEBUTTONUP:
                    pass

                #   Switch Controls   #
                #   Buttons Down
                elif ev.type == JOYBUTTONDOWN:
                    if ev.button == 1:  # B Button
                        self.activate('interact')

                    elif ev.button == 2:  # X Button
                        self.activate('special')
                    
                    elif ev.button == 3:  # Y Button
                        self.activate('attack1')
                        self.activate('attack2')

                    
                    elif ev.button == 0:  # A Button
                        self.activate('evasive')
                    
                    elif ev.button == 9:  # Start Button
                        self.activate('pause')

                #   Buttons Up
                elif ev.type == JOYBUTTONUP:
                    if ev.button == 1:  # B Button
                        self.deactivate('interact')

                    elif ev.button == 2:  # X Button
                        self.deactivate('special')
                    
                    elif ev.button == 3:  # Y Button
                        self.deactivate('attack1')
                        self.deactivate('attack2')

                    
                    elif ev.button == 0:  # A Button
                        self.deactivate('evasive')
                    
                    elif ev.button == 9:  # Start Button
                        self.deactivate('pause')

                  

                #   Analog Stick Motion
                elif ev.type == JOYAXISMOTION:
                    if ev.axis == 0:  # Left Analog Stick X Axis
                        if ev.value < -self.deadzone:
                            if not self.axis_left_active:
                                self.activate('motion_left')
                                self.axis_left_active = True
                        else:
                            if self.axis_left_active:
                                self.deactivate('motion_left')
                                self.axis_left_active = False
                        
                        if ev.value > self.deadzone:
                            if not self.axis_right_active:
                                self.activate('motion_right')
                                self.axis_right_active = True
                        else:
                            if self.axis_right_active:
                                self.deactivate('motion_right')
                                self.axis_right_active = False
                    
                    elif ev.axis == 1:  # Left Analog Stick Y Axis
                        if ev.value < -self.up_deadzone:
                            if not self.axis_up_active:
                                self.activate('motion_up')
                                self.axis_up_active = True
                        else:
                            if self.axis_up_active:
                                self.deactivate('motion_up')
                                self.axis_up_active = False
                        
                        if ev.value > self.down_deadzone:
                            if not self.axis_down_active:
                                self.activate('motion_down')
                                self.axis_down_active = True
                        else:
                            if self.axis_down_active:
                                self.deactivate('motion_down')
                                self.axis_down_active = False

            return True