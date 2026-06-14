def in_position(self) -> bool:
        #   Facing Right
        if self.vel[0] > 0:
            return int(self.position[0]) == int(player_position[0] + self.cam_delta)
        
        #   Facing Left
        elif self.vel[0] < 0:
            return int(self.position[0]) == int(player_position[0] - self.cam_delta)
        
        #   Idle
        else:
            return int(self.position[0]) == int(player_position[0])