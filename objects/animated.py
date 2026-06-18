from pygame import transform

from . import Drawable
from globals import vec
from UI import SpriteManager

SM = SpriteManager.getInstance()

class State(object):
    """Represents a state of animation"""
    def __init__(self, file_name = 'null.png',
                 starting_frame = 0, row = 0, fps = 8, num_frames = 1,
                 loop = False, loop_start = 0, loop_end = 0,
                 flip_x = False, flip_y = False):
        
        #   Keep track of the state's data  #
        self.file_name = file_name
        self.starting_frame = starting_frame
        self.row = row
        self.fps = fps
        self.num_frames = num_frames
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.loop = loop
        self.loop_start = loop_start
        self.loop_end = loop_end
        self.frames = {}
        

    def load_frames(self):
        for i in range(self.num_frames):
            self.frames[i] = SM.getSprite(self.file_name, (i, self.row))

    def get_file_name(self) -> str:
        return self.file_name
    
    def get_row(self) -> int:
        return self.row
    
    def get_fps(self) -> int:
        return self.fps
    
    def get_num_frames(self) -> int:
        return self.num_frames
    
    def get_starting_frame(self) -> int:
        return self.starting_frame
    
    

class Animated(Drawable):
    """Represents a Drawable object that can be Animated"""
    def __init__(self, position=vec(0,0), file_name="null.png", offset=None,
                 idle_state = State(), enemy = False):
        super().__init__(position, file_name, offset, enemy)

        #   State Data
        self.states = {'idle':idle_state}
        self.state = 'idle'
        self.frame = 0
        self.animation_timer = 0.0
        self.file_name = file_name
        self.switching_states = False
        self.next_state = ""
        self.last_frame = 0

        #   Data for playing a specific animation
        self.playing_animation = False
        self.current_animation = ""
        self.animation_frame = 0
        self.animation_start = 0
        self.animation_end = 0

    def get_state(self, state: str) -> State:
        return self.states[state]
    
    def get_current_state(self) -> State:
        return self.states[self.state]
    
    def get_num_frames(self) -> int:
        return self.get_current_state().get_num_frames()
    
    def get_fps(self) -> int:
        return self.get_current_state().get_fps()

    def get_row(self) -> int:
        return self.get_current_state().get_row()
    
    def set_state(self, state) -> None:
        """Set the current state to the given state"""
        self.state = state
        self.frame = self.get_current_state().get_starting_frame()
        self.set_image()

    def add_state(self, name: str, state: State) -> None:
        """Add a state to the state dictionary"""
        self.states[name] = state
    
    def del_state(self, name: str) -> None:
        """Remove a state from the state dictionary"""
        del self.states[name]

    def play_animation(self, state, starting_frame, ending_frame):
        """Play an animation without switching states"""
        self.playing_animation = True
        self.current_animation = state
        self.animation_start = starting_frame
        self.animation_end = ending_frame

    def set_image(self, pre_loaded = False, player = False) -> None:
        """Set the object's image"""
        if pre_loaded:
            #   Get the current state and the image
            if self.playing_animation:
                current_state = self.get_state(self.current_animation)
                new_image = current_state.frames[self.animation_frame]

            else:
                current_state = self.get_current_state()
                new_image = current_state.frames[self.frame]

            #   Transform the image if needed
            if current_state.flip_x or current_state.flip_y:
                new_image = transform.flip(new_image, current_state.flip_x, current_state.flip_y)

            #   Set the image
            if player:
                #   Must call drawable here
                Drawable.set_image(self, new_image)
            else:
                super().set_image(new_image)

        else:
            #   Get the current state's information
            current_state = self.get_current_state()
            file_name = current_state.get_file_name()
            row = current_state.get_row()

            #   Define and Set the image   #
            new_image = SM.getSprite(file_name, (self.frame, row))
            if current_state.flip_x or current_state.flip_y:
                new_image = transform.flip(new_image, current_state.flip_x, current_state.flip_y)
            super().set_image(new_image)
    
    def update(self, seconds):
        """Update the animation"""
        if self.animation_timer >= (1/self.get_fps()):
            if self.playing_animation:
                self.animation_frame += 1
                if self.animation_frame == self.animation_end + 1:
                    self.playing_animation = False
                else:
                    self.animation_timer = 0.0
                    self.set_image()
            else:
                #   Get the current state
                current_state = self.get_current_state()

                #   Finish the animation before the next
                if self.switching_states:
                    if self.frame == self.last_frame:
                        self.state = self.next_state
                        self.frame = self.get_current_state().get_starting_frame()
                        self.animation_timer = 0.0
                        self.switching_states = False
                        self.set_image()
                        return
                    else:
                        self.frame += 1
                        self.animation_timer = 0.0
                        self.set_image()
                        return

                #   Loop the animation if needed
                if current_state.loop and self.frame >= current_state.loop_start:
                    if self.frame == current_state.loop_end:
                        self.frame = current_state.loop_start
                    else:
                        self.frame += 1

                #   Progress the animation normally
                else:
                    self.frame += 1
                    self.frame %= self.get_num_frames()
                    
                #   Reset the timer and set the image
                self.animation_timer = 0.0
                self.set_image()
        else:
            self.animation_timer += seconds