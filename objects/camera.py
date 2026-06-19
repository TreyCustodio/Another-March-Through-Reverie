from globals import vec, SCREEN_SIZE, UPSCALED

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
    
    def in_position(self, player_position, player_velocity, player_direction) -> bool:
        #   Facing Right
        if player_velocity[0] > 0:
            return int(self.position[0]) == int(player_position[0] + self.delta)
        
        #   Facing Left
        elif player_velocity[0] < 0:
            return int(self.position[0]) == int(player_position[0] - self.delta)
        
        #   Idle
        else:
            return int(self.position[0]) == int(player_position[0])
    
    def set_position(self, player_position, direction, lock=False) -> None:
        """
        Set the camera's position to the desired position.
        Directions:
        0 -> right; 1 -> left; 2 -> idle
        """

        #   Facing Right
        if direction == "right":
            if lock:
                self.position[0] = int(player_position[0])
            else:
                self.position[0] = int(player_position[0] + self.delta)
            self.frame_counter = 0

        #   Facing Left
        elif direction == "left":
            if lock:
                self.position[0] = int(player_position[0])
            else:
                self.position[0] = int(player_position[0] - self.delta)
            self.frame_counter = 0

        #   Idle
        else:
            if direction == "right":
                self.position[0] = int(player_position[0])
            elif direction == "left":
                self.position[0] = int(player_position[0])
    
    def update(self, seconds, player_position, player_velocity,
               player_size, player_direction, max_player_speed) -> None:
        """Position the camera as desired"""
        #   Keep the player centered during camera lock
        if self.locked:
            if self.in_position(player_position, player_velocity, player_direction):
                return
            else:
                if player_velocity[0] > 0:
                    self.set_position(player_position, player_direction, lock=True)
                elif player_velocity[0] < 0:
                    self.set_position(player_position, player_direction, lock=True)
                else:
                    self.set_position(player_position, player_direction, lock=True)
            return
        
        #   Check if the camera is in the desired position
        if self.in_position(player_position, player_velocity, player_direction):
            return

        #   Update the camera's position
        else:
            #   Player running at max speed or above; camera catches up fast
            if abs(player_velocity[0]) >= max_player_speed:
                #   Moving Right
                if player_velocity[0] > 0:
                    if self.position[0] < int(self.position[0] + self.delta):
                        self.position[0] += (self.catch) * seconds
                        
                        if self.position[0] >= int(self.position[0] + self.delta):
                            self.set_position(player_position, player_direction)

                #   Moving Left
                elif player_velocity[0] < 0 :
                    if self.position[0] > int(self.position[0] - self.delta):
                        self.position[0] -= (self.catch) * seconds
                        
                        if self.position[0] <= int(self.position[0] - self.delta):
                            self.set_position(player_position, player_direction)

            #    Player running slower than max speed; cam moves with the player
            else:
                #   Moving Right
                if player_velocity[0] > 0:
                    if self.position[0] < int(self.position[0] + self.delta):
                        self.position[0] += (player_velocity[0] + self.speed) * seconds
                        
                        if self.position[0] >= int(self.position[0] + self.delta):
                            self.set_position(player_position, player_direction)


                #   Moving Left
                elif player_velocity[0] < 0:
                    if self.position[0] > int(self.position[0] - self.delta):

                        self.position[0] += (player_velocity[0] - self.speed) * seconds
                        
                        if self.position[0] <= int(self.position[0] - self.delta):
                            self.set_position(player_position, player_direction)


                #   At rest
                else:
                    #   Camera too far left; move it right
                    if self.frame_counter == self.idle_frames:
                        if self.position[0] < int(self.position[0]):
                            self.position[0] += (self.speed * 2) * seconds
                            if self.position[0] >= int(self.position[0]):
                                self.set_position(player_position, player_direction)

                        #   Camera too far right; move it left
                        elif self.position[0] > int(self.position[0]):
                            self.position[0] -= (self.speed * 2) * seconds
                            if self.position[0] <= int(self.position[0]):
                                self.set_position(player_position, player_direction)
                    else:
                        self.frame_counter += 1
        return