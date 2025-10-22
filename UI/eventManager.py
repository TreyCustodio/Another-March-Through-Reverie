from pygame import event
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
                #   Action Commands
                'interact': False,
                'attack1': False,
                'space': False,

                #   Movement (Arrow keys, WASD, Controller Analog stick)
                'motion_down': False,
                'motion_left': False,
                'motion_up': False,
                'motion_right': False,

                #   Mouse Motion
            }

            self.quit = False
        
        def QUIT(self):
            self.quit = True

        def activate(self, action):
            if action in self.actions:
                self.actions[action] = True
        
        def deactivate(self, action):
            if action in self.actions:
                self.actions[action] = False

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

        def update_buffer(self, seconds) -> None:
            """Update the buffer value for certain inputs such as moving through menus"""
            return

        def main(self, print_events = False) -> bool:
            """Get events from the pygame event queue and interpret them"""
            if self.quit:
                return False
            
            for ev in event.get():
                if print_events:
                    print(ev, end="\n\n")

                if ev.type == QUIT:
                    return False
                

                #   Keyboard Controls   #
                #   Keys Down
                elif ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        return False
                    
                    elif ev.key == K_z:
                        self.activate('interact')
                    
                    elif ev.key == K_x:
                        self.activate('attack1')

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
                    if ev.key == K_z:
                        self.deactivate('interact')
                    
                    elif ev.key == K_x:
                        self.deactivate('attack1')

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

                #   Mouse Controls  #
                elif ev.type == MOUSEMOTION:
                    pass
                
                elif ev.type == MOUSEBUTTONDOWN:
                    pass

                elif ev.type == MOUSEBUTTONUP:
                    pass

            return True