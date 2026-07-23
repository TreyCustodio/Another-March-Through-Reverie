from globals import vec, SCREEN_SIZE, UPSCALED, PLAYER_SCALE
from . import Drawable

PLAYER_WIDTH = int(48 * PLAYER_SCALE)
PLAYER_HEIGHT = int(48 * PLAYER_SCALE)

class Camera:
    """The Camera"""
    def __init__(self, position):
        #   Cast the camera position to integer values
        self.position = vec(int(position[0]), int(position[1]))
        self.speed = 20
        self.catch = 900
        self.delta = 50
        self.locked = False
        self.idle_frames = 32
        self.frame_counter = 32
        self.vel = vec(0,0)
        


    def get_position(self) -> vec:
        return self.position.copy()
    
    def update(self, seconds, player_position, player_velocity,
               player_size, player_direction, max_player_speed) -> None:
        """Position the camera as desired"""
        self.position[0] = int(player_position[0]) + (PLAYER_WIDTH // 2)
        self.position[1] = int(player_position[1]) + (PLAYER_HEIGHT // 2)
        return
    
        d_x = 16
        target_x = int(player_position[0]) + (PLAYER_WIDTH // 2)
        target_y = int(player_position[1]) + (PLAYER_HEIGHT // 2)

        if player_direction == "left":
            target_x -= d_x
        elif player_direction == "right":
            target_x += d_x

        smoothing = min(1.0, seconds * self.speed)

        self.position[0] += (target_x - self.position[0]) * smoothing
        self.position[1] += (target_y - self.position[1]) * smoothing

        #   Optional display routine
        print("=========================")
        print("Camera Position:", self.position)
        print("Player Position:",player_position)
        print("Difference:", vec(abs(player_position[0] - self.position[0]), abs(player_position[1] - self.position[1])))
        print("=========================\n\n\n\n\n")