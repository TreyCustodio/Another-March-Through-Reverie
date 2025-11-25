from . import Drawable
from globals import vec
from UI import SpriteManager

SM = SpriteManager.getInstance()

class State(object):
    """Represents a state of animation"""
    def __init__(self, file_name = 'null.png',
                 starting_frame = 0, row = 0, fps = 8, num_frames = 1):
        #   Keep track of the state's data  #
        self.file_name = file_name
        self.starting_frame = starting_frame
        self.row = row
        self.fps = fps
        self.num_frames = num_frames

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

        self.states = {'idle':idle_state}
        self.state = 'idle'
        self.frame = 0
        self.animation_timer = 0.0
        self.file_name = file_name

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

    def set_image(self) -> None:
        """Set the object's image"""
        #   Get the current state's information #
        current_state = self.get_current_state()
        file_name = current_state.get_file_name()
        row = current_state.get_row()

        #   Define and Set the image   #
        new_image = SM.getSprite(file_name, (self.frame, row))
        super().set_image(new_image)
    
    def update(self, seconds):
        """Update the animation"""
        if self.animation_timer >= (1/self.get_fps()):
            self.frame += 1
            self.frame %= self.get_num_frames()
            self.animation_timer = 0.0
            self.set_image()
        else:
            self.animation_timer += seconds