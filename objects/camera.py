from globals import vec, SCREEN_SIZE, UPSCALED
from . import Drawable

class Camera:
    """The Camera"""
    def __init__(self, position):
        #   Cast the camera position to integer values
        self.position = vec(int(position[0]), int(position[1]))
        self.speed = 40
        self.catch = 900
        self.delta = 50
        self.locked = False
        self.idle_frames = 32
        self.frame_counter = 32




    def get_position(self) -> vec:
        return self.position.copy()
    
    def update(self, seconds, player_position, player_velocity,
               player_size, player_direction, max_player_speed) -> None:
        """Position the camera as desired"""
        self.position[0] = int(player_position[0]) + (player_size[0] // 2)
        self.position[1] = int(player_position[1]) + (player_size[1] // 2)

        #   Optional display routine
        # print("=========================")
        # print("Camera Position:", self.position)
        # print("Player Position:",player_position)
        # print("=========================\n")