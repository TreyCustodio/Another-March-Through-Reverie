import os

from pygame import font, Rect

from globals import vec, GRAVITY, UPSCALED
from UI import EventManager, AudioManager, SpriteManager
from . import Drawable, State


EM = EventManager.getInstance()
AM = AudioManager.getInstance()
SM = SpriteManager.getInstance()


class PlayerLoader:
    _INSTANCE = None

    @classmethod
    def get_player(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = Player()
        return cls._INSTANCE
    

class Player(Drawable):
    def __init__(self, position=vec(0,0)):
        super().__init__(position, file_name="samus.png", offset=(0,0))

        #   State Dictionary    #
        self.states = {
            # state: [file_name, row, fps, nFrames, starting_frame]
            'idle': State("samus.png", starting_frame=0, row=0, fps=8, num_frames=3),
            'idle_right': State("samus.png", 0, 10, 12, 3),
            'idle_left': State("samus.png", 0, 11, 12, 3),

            'walking_right': State("samus.png", 0, 1, 24, 10),
            'walking_left': State("samus.png", 0, 2, 24, 10),
            
            'jumping_right': State("samus.png", 0, 3, 32, 10),
            'jumping_left': State("samus.png", 0, 4, 32, 10),
        }

        #   Animation Properties    #
        self.state = 'idle'
        self.frame = 0
        self.animation_timer = 0.0
        self.shadow = Drawable(vec(self.position[0] - 8, self.position[1]), "samus.png", (0,0))

        #   Camera Properties   #
        p = position.copy()
        self.cam_pos = vec(int(p[0]), int(p[1]))
        self.camera_speed = 40
        self.camera_catch = 900
        self.cam_delta = 50
        self.camera_lock = False
        self.idle_counter = 32
        self.idle_frames = 32

        #   Physics Variables   #
        self.speed = 75
        self.max_speed = 600
        self.weight = 15
        self.acceleration = 120
        self.deceleration = 120
        self.boost_deceleration = 10
        self.jump_force = -200
        self.jump_force_max = -400
        self.boost_force = 1200
        self.vel = vec(0,0)

        #   Physics States  #
        self.airborn = False
        self.gaining = False
        self.boosting = False
        self.idle = True
        self.crouching = True
        self.visible = False # If False, the player is not considered in the engine


    def set_visible(self):
        self.visible = True

    def set_invisible(self):
        self.visible = False
    
    def lock_camera(self):
        self.camera_lock = True

    def free_camera(self):
        self.camera_lock = False

    def get_collision_rect(self):
        return Rect(self.position, (self.get_width(), self.get_height()))
        
    def draw(self, drawSurf):
        if not self.visible:
            return
        
        if self.state == 'idle':
            pass

        else:
            #   Draw Max Speed Shadow   #
            if abs(self.vel[0]) >= self.max_speed:
                if self.state == 'walking_left' or self.state == 'jumping_left':
                    self.shadow.set_position(vec(self.position[0] + 18, self.position[1]))
                    self.shadow.draw(drawSurf)
                    self.shadow.set_position(vec(self.position[0] + 12, self.position[1]))
                    self.shadow.draw(drawSurf)
                    self.shadow.set_position(vec(self.position[0] + 6, self.position[1]))
                    self.shadow.draw(drawSurf)
                
                elif self.state == 'walking_right' or self.state == 'jumping_right':
                    self.shadow.set_position(vec(self.position[0] - 18, self.position[1]))
                    self.shadow.draw(drawSurf)
                    self.shadow.set_position(vec(self.position[0] - 12, self.position[1]))
                    self.shadow.draw(drawSurf)
                    self.shadow.set_position(vec(self.position[0] - 6, self.position[1]))
                    self.shadow.draw(drawSurf)
                        
            elif abs(self.vel[0]) >= ((self.max_speed // 3) * 2):
                if self.state == 'walking_left' or self.state == 'jumping_left':
                    self.shadow.set_position(vec(self.position[0] + 12, self.position[1]))
                    self.shadow.draw(drawSurf)
                    self.shadow.set_position(vec(self.position[0] + 6, self.position[1]))
                    self.shadow.draw(drawSurf)
                
                elif self.state == 'walking_right' or self.state == 'jumping_right':
                    self.shadow.set_position(vec(self.position[0] - 12, self.position[1]))
                    self.shadow.draw(drawSurf)
                    self.shadow.set_position(vec(self.position[0] - 6, self.position[1]))
                    self.shadow.draw(drawSurf)

            elif abs(self.vel[0]) >= ((self.max_speed // 3)):
                if self.state == 'walking_left' or self.state == 'jumping_left':
                    self.shadow.set_position(vec(self.position[0] + 6, self.position[1]))
                    self.shadow.draw(drawSurf)
                
                elif self.state == 'walking_right' or self.state == 'jumping_right':
                    self.shadow.set_position(vec(self.position[0] - 6, self.position[1]))
                    self.shadow.draw(drawSurf)
        
        #   Display the velocity    #
        # velocity = str(round(self.vel[0], 2))
        # img = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16).render("Velocity: " + str(velocity), False, (255,255,255), (0,0,0))
        # drawSurf.blit(img, vec(self.position[0] + self.get_width() // 2 - img.get_width() // 2, self.position[1] - img.get_height() - 8) - Drawable.CAMERA_OFFSET)
        

        
        super().draw(drawSurf)

    def set_position(self, position):
        self.position = position
        self.cam_pos = position.copy()

    def set_image(self):
        current_state = self.get_current_state()
        file_name = current_state.get_file_name()
        row = current_state.get_row()

        new_image = SM.getSprite(file_name, (self.frame, row))
        super().set_image(new_image)

        shadow_image = SM.getSprite('samus.png', (self.frame, row+5))
        self.shadow.set_image(shadow_image)

    def get_current_state(self):
        return self.states[self.state]
    
    def get_num_frames(self):
        return self.get_current_state().get_num_frames()
    
    def get_fps(self):
        return self.get_current_state().get_fps()

    def get_row(self):
        return self.get_current_state().get_row()

    def set_state(self, state):
        self.state = state
        self.frame = self.get_current_state().get_starting_frame()
        self.set_image()

    def set_idle(self, direction = 'down'):
        if direction == 'down':
            self.set_state('idle')

        elif direction == 'left':
            self.set_state('idle_left')
            
        elif direction == 'right':
            self.set_state('idle_right')

        self.idle = True


    def walking(self) -> bool:
        return self.state == 'walking_left' or self.state == 'walking_right'
    
    def jumping(self) -> bool:
        return self.state == 'jumping_left' or self.state == 'jumping_right'
    
    def move(self):
        self.idle = False
        self.crouching = False

    def handle_events(self):
        if not self.visible:
            return
        
        #   Left Motion #
        if EM.is_active('motion_left'):

            #   Jump Left
            if self.state == 'jumping_right':
                self.set_state('jumping_left')
                if self.vel[0] >= self.max_speed:
                    self.vel[0] *= -1
                else:
                    self.vel[0] = -self.speed

            #   Walk Left
            elif self.state != 'walking_left' and not self.jumping():
                self.move()
                self.set_state('walking_left')
                EM.deactivate('motion_right')

                if abs(self.vel[0]) >= self.max_speed:
                    self.vel[0] *= -1
                else:
                    self.vel[0] = -self.speed

        else:
            #   Idle
            if not self.idle and not self.jumping() and self.state != 'walking_right':
                self.set_idle('left')

        #   Right Motion    #
        if EM.is_active('motion_right'):

            #   Jump Right
            if self.state == 'jumping_left':
                self.set_state('jumping_right')
                if abs(self.vel[0]) >= self.max_speed:
                    self.vel[0] *= -1
                else:
                    self.vel[0] = self.speed

            #   Walk Right
            elif self.state != 'walking_right' and not self.jumping():
                self.move()
                self.set_state('walking_right')
                EM.deactivate('motion_left')
                if abs(self.vel[0]) >= self.max_speed:
                    self.vel[0] *= -1
                else:
                    self.vel[0] = self.speed

        else:
            #   Idle
            if not self.idle and not self.jumping() and self.state != 'walking_left':
                self.set_idle('right')


        if EM.is_active('motion_up'):
            pass

        if EM.is_active('motion_down'):
            if not self.crouching:
                self.set_idle('down')
                self.vel[0] = 0
                self.crouching = True
        
        #   Jumping #
        if EM.is_active('interact'):
            #   Second Jump Press   #
            if not self.gaining:
                if self.airborn:
                    if not self.boosting:
                        #   Boost (1st upgrade)   #
                        if self.state == "jumping_left":
                        # if self.vel[0] <= 0:
                            self.vel[0] = -self.boost_force

                        else:
                            self.vel[0] = self.boost_force
                        
                        self.boosting = True

                #   Jump    #
                else:
                    self.vel[1] = self.jump_force
                    self.airborn = True
                    self.gaining = True

                    if self.state == 'walking_left' or self.state == 'idle_left':
                        self.set_state('jumping_left')

                    elif self.state == 'walking_right' or self.state == 'idle_right':
                        self.set_state('jumping_right')
                    
                    else:
                        self.set_state('jumping_left')

            #   Do nothing while gaining
        
        else:
            #   Stop gaining after button is released
            if self.airborn:
                self.gaining = False


        if EM.is_active('attack1'):
            pass

        return
    
    def accel(self, seconds):
        """Accelerate to max speed and stay at that speed"""
        #   Moving Right    #
        if self.vel[0] > 0:
            self.vel[0] += self.acceleration * seconds
            if self.vel[0] > self.max_speed:
                self.vel[0] = self.max_speed
        elif self.vel[0] < 0:
            self.vel[0] -= self.acceleration * seconds
            if self.vel[0] < -self.max_speed:
                self.vel[0] = -self.max_speed

    def decel(self, seconds):
        """Decelerate to max speed and stay at that speed"""
        #   Moving Right    #
        if self.vel[0] > 0:
            self.vel[0] -= (self.deceleration * self.boost_deceleration) * seconds
            if self.vel[0] < 0:
                self.vel[0] = self.max_speed
       
       #    Moving Left #
        else:
            self.vel[0] += (self.deceleration * self.boost_deceleration) * seconds
            if self.vel[0] > 0:
                self.vel[0] = -self.max_speed

    def stop(self, seconds):
        """Decelerate to 0 and stop"""
        #   Moving Right    #
        if self.vel[0] > 0:
            self.vel[0] -= (self.deceleration * self.weight) * seconds
            if self.vel[0] < 0:
                self.vel[0] = 0
                #   Begin the idle animation
                if self.state == "walking_right":
                    self.set_idle("right")
        
        #   Moving Left #
        else:
            self.vel[0] += (self.deceleration * self.weight) * seconds
            if self.vel[0] > 0:
                self.vel[0] = 0
                #   Begin the idle animation
                if self.state == "walking_left":
                    self.set_idle("left")

    def update_vertical(self, seconds):
        """Update the player's vertical (y axis) velocity"""
        #   In the air  #
        if self.airborn:
            #   Check if the player is on the ground and update their state
            if self.position[1] >  UPSCALED[1] - UPSCALED[1] // 4 - self.get_height():
                #   Reset states
                self.airborn = False
                self.slowing_down = False
                self.gaining = False
                self.boosting = False

                #   Set the y position and velocity
                self.position[1] = UPSCALED[1] - UPSCALED[1] // 4 - self.get_height()
                self.vel[1] = 0

                #  Reset animation
                if self.vel[0] < 0:
                    self.set_state('walking_left')
                
                elif self.vel[0] > 0:
                    self.set_state('walking_right')
                
                else:
                    self.set_state('idle')

                #   Deactivate the interact button
                EM.deactivate('interact')
                
            #   Enforce gravity on the vertical velocity
            else:
                self.vel[1] += GRAVITY * seconds

    def update_horizontal(self, seconds):
        """Update the player's horizontal (x axis) velocity"""
        #   Decel to 0
        if self.idle:
            self.stop(seconds)
        else:
            #   Accel to max speed
            if abs(self.vel[0]) < self.max_speed:
                self.accel(seconds)
                
            #   Deccel to max speed
            else:
                if abs(self.vel[0]) > self.max_speed:
                    self.decel(seconds)

    def update_movement(self, seconds):
        """
        Update the player's position and velocity.
        v_new = (v_old + acceleration) * seconds
        """
        #   Running up a slope  #
        #   self.vel = self.vel + SLOPE * seconds
        
        #   Vertical Velocity Control   #
        self.update_vertical(seconds)
        
        #   Horizontal Velocity Control #
        self.update_horizontal(seconds)
        
        #   Set Position    #
        self.position += self.vel*seconds

    def set_camera_position(self, direction=0, lock = False):
        """
        Set the camera's position to the desired position.
        Directions:
        0 -> right; 1 -> left; 2 -> idle
        """

        #   Facing Right
        if direction == 0:
            if lock:
                self.cam_pos[0] = int(self.position[0])
            else:
                self.cam_pos[0] = int(self.position[0] + self.cam_delta)
            self.idle_counter = 0

        #   Facing Left
        elif direction == 1:
            if lock:
                self.cam_pos[0] = int(self.position[0])
            else:
                self.cam_pos[0] = int(self.position[0] - self.cam_delta)
            self.idle_counter = 0

        #   Idle
        else:
            self.cam_pos[0] = int(self.position[0])
    
    def camera_in_position(self):
        """Check if the camera is in the desired position"""
        #   Facing Right
        if self.vel[0] > 0:
            return int(self.cam_pos[0]) == int(self.position[0] + self.cam_delta)
        
        #   Facing Left
        elif self.vel[0] < 0:
            return int(self.cam_pos[0]) == int(self.position[0] - self.cam_delta)
        
        #   Idle
        else:
            return int(self.cam_pos[0]) == int(self.position[0])

    def update_camera(self, seconds):
        """Position the camera as desired"""
        #   Keep the player centered during camera lock
        if self.camera_lock:
            if self.camera_in_position():
                return
            else:
                if self.vel[0] > 0:
                    self.set_camera_position(0, lock=True)
                elif self.vel[0] < 0:
                    self.set_camera_position(1, lock=True)
                else:
                    self.set_camera_position(2, lock=True)
            return
        
        #   Check if the camera is in the desired position
        if self.camera_in_position():
            return

        #   Update the camera's position
        else:
            #   Player running at max speed or above; camera catches up fast
            if abs(self.vel[0]) >= self.max_speed:
                #   Moving Right
                if self.vel[0] > 0:
                    if self.cam_pos[0] < int(self.position[0] + self.cam_delta):
                        self.cam_pos[0] += (self.camera_catch) * seconds
                        
                        if self.cam_pos[0] >= int(self.position[0] + self.cam_delta):
                            self.set_camera_position(0)

                #   Moving Left
                elif self.vel[0] < 0 :
                    if self.cam_pos[0] > int(self.position[0] - self.cam_delta):
                        self.cam_pos[0] -= (self.camera_catch) * seconds
                        
                        if self.cam_pos[0] <= int(self.position[0] - self.cam_delta):
                            self.set_camera_position(1)

            #    Player running slower than max speed; cam moves with the player
            else:
                #   Moving Right
                if self.vel[0] > 0:
                    if self.cam_pos[0] < int(self.position[0] + self.cam_delta):
                        self.cam_pos[0] += (self.vel[0] + self.camera_speed) * seconds
                        
                        if self.cam_pos[0] >= int(self.position[0] + self.cam_delta):
                            self.set_camera_position(0)


                #   Moving Left
                elif self.vel[0] < 0:
                    if self.cam_pos[0] > int(self.position[0] - self.cam_delta):

                        self.cam_pos[0] += (self.vel[0] - self.camera_speed) * seconds
                        
                        if self.cam_pos[0] <= int(self.position[0] - self.cam_delta):
                            self.set_camera_position(1)


                #   At rest
                else:
                    #   Camera too far left; move it right
                    if self.idle_counter == self.idle_frames:
                        if self.cam_pos[0] < int(self.position[0]):
                            self.cam_pos[0] += (self.camera_speed * 2) * seconds
                            if self.cam_pos[0] >= int(self.position[0]):
                                self.set_camera_position(2)

                        #   Camera too far right; move it left
                        elif self.cam_pos[0] > int(self.position[0]):
                            self.cam_pos[0] -= (self.camera_speed * 2) * seconds
                            if self.cam_pos[0] <= int(self.position[0]):
                                self.set_camera_position(2)
                    else:
                        self.idle_counter += 1

                    

    

    
    
    def update(self, seconds):
        if not self.visible:
            return
        
        #   Update Animation    #
        if self.animation_timer >= (1/self.get_fps()):
            self.frame += 1
            self.frame %= self.get_num_frames()
            self.animation_timer = 0.0
            self.set_image()
        else:
            self.animation_timer += seconds

        #   Update Physics  #
        self.update_movement(seconds)

        #   Update Camera Position  #
        self.update_camera(seconds)
