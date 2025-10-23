import os

from pygame import font, Rect

from globals import vec, GRAVITY, UPSCALED
from UI import EventManager, AudioManager, SpriteManager
from . import Drawable


EM = EventManager.getInstance()
AM = AudioManager.getInstance()
SM = SpriteManager.getInstance()


class State(object):
    def __init__(self, file_name, starting_frame, row, fps, num_frames):
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

        #   Physics #
        self.speed = 75
        self.max_speed = 600
        self.weight = 15

        self.acceleration = 120
        self.boost_deceleration = 10
        self.jump_force = -200
        self.jump_force_max = -400
        self.boost_force = self.max_speed*2
        self.vel = vec(0,0)

        #   Physics States  #
        self.airborn = False
        self.gaining = False
        self.boosting = False
        self.idle = True
        self.crouching = True

        #   Start BGM   #
        AM.play_ost("HS")

    def get_collision_rect(self):
        return Rect(self.position, (self.get_width(), self.get_height()))
        
    def draw(self, drawSurf):
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

        velocity = str(round(self.vel[0], 2))
        img = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16).render("Velocity: " + str(velocity), False, (255,255,255), (0,0,0))
        drawSurf.blit(img, vec(self.position[0] + self.get_width() // 2 - img.get_width() // 2, self.position[1] - img.get_height() - 8) - Drawable.CAMERA_OFFSET)
        

        
        super().draw(drawSurf)


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
    
    def update(self, seconds):
        #   Update Animation    #
        if self.animation_timer >= (1/self.get_fps()):
            self.frame += 1
            self.frame %= self.get_num_frames()
            self.animation_timer = 0.0
            self.set_image()
        else:
            self.animation_timer += seconds

        #   Update Physics  #
        #   v_new = (v_old + acceleration) * seconds

        #   This code would work for a slope
        #   self.vel = self.vel + SLOPE * seconds
        

        #   Vertical Velocity Control   #
        if self.airborn:
            #   Hit the ground; stop jumping
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

            #   Otherwise enforce gravity
            else:
                self.vel[1] += GRAVITY * seconds
        
        #   Horizontal Velocity Control #
        if self.idle:
            self.stop(seconds)
        
        else:
            #   Accel
            if abs(self.vel[0]) < self.max_speed:
                self.accel(seconds)
                
            #   Deccel
            else:
                if abs(self.vel[0]) > self.max_speed:
                    self.decel(seconds)
            

        self.position += self.vel*seconds
        return
    
    def accel(self, seconds):
        #   Accelerate to max speed and stay there
        if self.vel[0] > 0:
            self.vel[0] += self.acceleration * seconds
            if self.vel[0] > self.max_speed:
                self.vel[0] = self.max_speed
        elif self.vel[0] < 0:
            self.vel[0] -= self.acceleration * seconds
            if self.vel[0] < -self.max_speed:
                self.vel[0] = -self.max_speed

    def decel(self, seconds):
        #   Decelerate to max speed and stay there
        if self.vel[0] > 0:
            self.vel[0] -= (self.acceleration * self.boost_deceleration) * seconds
            if self.vel[0] < 0:
                self.vel[0] = self.max_speed
        else:
            self.vel[0] += (self.acceleration * self.boost_deceleration) * seconds
            if self.vel[0] > 0:
                self.vel[0] = -self.max_speed
        

    def stop(self, seconds):
        #   Decelerate to 0 and stay there  #
        #   Facing Right
        if self.vel[0] > 0:
            self.vel[0] -= (self.acceleration * self.weight) * seconds
            if self.vel[0] < 0:
                self.vel[0] = 0
                if self.state == "walking_right":
                    self.set_idle("right")
        
        #   Facing Left
        else:
            self.vel[0] += (self.acceleration * self.weight) * seconds
            if self.vel[0] > 0:
                self.vel[0] = 0
                if self.state == "walking_left":
                    self.set_idle("left")
        