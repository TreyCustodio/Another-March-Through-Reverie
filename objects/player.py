import os

from pygame import font, Rect, transform

from globals import vec, GRAVITY, UPSCALED
from UI import EventManager, AudioManager, SpriteManager
from . import Drawable, State, Animated
from .camera import Camera

from .weapons import *


EM = EventManager.getInstance()
AM = AudioManager.getInstance()
SM = SpriteManager.getInstance()


class PlayerLoader:
    """Use this class to ensure that only one player is ever loaded"""
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
        ## original samus sprites
        # self.states = {
        #     # state: [file_name, row, fps, nFrames, starting_frame]
        #     'idle': State("samus.png", starting_frame=0, row=0, fps=16, num_frames=3),
        #     'idle_right': State("samus.png", 0, 10, 12, 3),
        #     'idle_left': State("samus.png", 0, 11, 12, 3),

        #     'walking_right': State("samus.png", 0, 1, 24, 10),
        #     'walking_left': State("samus.png", 0, 2, 24, 10),
            
        #     'jumping_right': State("samus.png", 0, 3, 32, 10),
        #     'jumping_left': State("samus.png", 0, 4, 32, 10),
        # }

        self.states = {
            # state: [file_name, starting_frame, row, fps, nFrames]
            'idle': State("weaver.png", starting_frame=0, row=0, fps=16, num_frames=48),
            'idle_right': State("weaver.png", 0, 0, 16, 48),
            'idle_left': State("weaver.png", 0, 1, 16, 48),

            'walking_right': State(file_name="weaver_walk.png", starting_frame=0, row=0, fps=16, num_frames=10),
            'walking_left': State("weaver_walk.png", 0, 0, 16, 10, flip_x=True),

            'running_right': State("weaver_run.png", 0, 0, 16, 9, flip_x=False),
            'running_left': State("weaver_run.png", 0, 0, 16, 9, flip_x=True),

            'crouching_right': State("weaver_crouch.png", 0, 0, 32, 11, loop=True, loop_start = 3, loop_end=5, flip_x=False),
            'crouching_left': State("weaver_crouch.png", 0, 0, 32, 11, loop=True, loop_start = 3, loop_end=5, flip_x=True),

            'shooting_right': State("weaver_shot.png", 0, 0, 64, 12, loop = True, loop_start = 3, loop_end = 8, flip_x=False),
            'shooting_left': State("weaver_shot.png", 0, 0, 64, 12, loop=True, loop_start = 3, loop_end = 8, flip_x=True),

            'jumping_right': State("weaver_jump.png", row = 0, starting_frame = 0, fps = 16, num_frames = 13),
            'jumping_left': State("weaver_jump.png", row = 1, starting_frame = 0, fps = 16, num_frames = 13),

        }
        
        for state in self.states:
            self.states[state].load_frames()

        #   Animation Properties    #
        self.state = 'idle'
        self.frame = 0
        self.animation_timer = 0.0
        self.switching_states = False
        self.next_state = ""
        self.last_frame = 0
        self.shadow = Drawable(vec(self.position[0] - 8, self.position[1]), "samus.png", (0,0))

        #   Data for playing a specific animation   #
        self.playing_animation = False
        self.current_animation = ""
        self.animation_frame = 0
        self.animation_start = 0
        self.animation_end = 0

        #   Set the initial image   #
        self.set_image()


        #   Camera Properties   #
        p = position.copy()
        self.camera = Camera(p)

        #   Physics Variables   #
        self.hp = 5
        self.max_hp = 5
        self.speed = 75
        self.max_speed = 600
        self.running_speed = 300
        self.weight = 15
        self.acceleration = 120
        self.deceleration = 120
        self.boost_deceleration = 10
        self.jump_force = -160
        self.jump_hold_max = 0.40
        self.jump_hold_time = 0.0
        self.jump_hold_gravity = 180
        self.boost_force = 800
        self.vel = vec(0,0)

        #   Weapon Variables    #
        self.shot_cooldown = 0.1
        self.cooldown_timer = 0.0

        #   Physics States  #
        self.attacking = False
        self.shot_ready = False
        self.cooling_down = False
        self.airborn = False
        self.gaining = False
        self.boosting = False
        self.idle = True
        self.crouching = False
        self.grounded = True  # True when player is on ground
        self.colliding = False
        self.visible = False # If False, the player is not considered in the engine
        self.vulnerable = True
        self.damage_cooldown = 0.75
        self.damage_timer = 0.0
        self.facing = 'right'  # current player facing direction

        #   Key Locking #
        self.key_lock = False

    def lock_keys(self):
        self.key_lock = True

    def unlock_keys(self):
        self.key_lock = False

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
    
    def draw_shadows(self, drawSurf):
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

    def draw(self, drawSurf):
        if not self.visible:
            return
        
        if self.state == 'idle':
            pass

        else:
            pass
            #   Draw Max Speed Shadow   #
            # self.draw_shadows(drawSurf)
            
        
        #   Display the velocity    #
        # velocity = str(round(self.vel[0], 2))
        # img = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16).render("Velocity: " + str(velocity), False, (255,255,255), (0,0,0))
        # drawSurf.blit(img, vec(self.position[0] + self.get_width() // 2 - img.get_width() // 2, self.position[1] - img.get_height() - 8) - Drawable.CAMERA_OFFSET)
        

        
        super().draw(drawSurf, False)

    def set_position(self, position):
        self.position = position
        self.cam_pos = position.copy()

    def set_image(self):
        Animated.set_image(self, pre_loaded=True, player = True)
        # shadow_image = SM.getSprite('samus.png', (self.frame, row+5))
        # self.shadow.set_image(shadow_image)

    def play_animation(self, state, starting_frame, ending_frame):
        """Play an animation without switching states"""
        Animated.play_animation(self, state, starting_frame, ending_frame)

    def get_current_state(self):
        return self.states[self.state]
    
    def get_num_frames(self):
        return self.get_current_state().get_num_frames()
    
    def get_fps(self):
        return self.get_current_state().get_fps()

    def get_row(self):
        return self.get_current_state().get_row()

    def set_state(self, state, finish_animation = False, last_frame = 0, optional_start_frame = -1):
        # print(state)
        #   Finish the current animation before proceeding to the next state
        if finish_animation:
            self.frame = self.get_current_state().loop_end
            self.next_state = state
            self.switching_states = True
            self.last_frame = last_frame

        #   Proceed to the next state
        else:
            self.state = state
            if optional_start_frame != -1:
                self.frame = optional_start_frame
            else:
                self.frame = self.get_current_state().get_starting_frame()

        #   Set the image
        self.set_image()

    def set_idle(self, direction = 'down'):
        if direction == 'down':
            if self.facing == 'left':
                self.set_state('idle_left')
            else:
                self.set_state('idle_right')

        elif direction == 'left':
            self.set_state('idle_left')
            self.facing = 'left'
            
        elif direction == 'right':
            self.set_state('idle_right')
            self.facing = 'right'

        self.idle = True

    def crouch(self):
        self.vel[0] = 0
        self.crouching = True
        if self.facing == 'right':
            self.set_state('crouching_right')
        elif self.facing == 'left':
            self.set_state('crouching_left')

    def exit_crouch(self):
        EM.deactivate('interact')
        self.crouching = False
        self.lock_keys()
        if self.facing == "right":
            self.set_state("idle_right", finish_animation=True, last_frame=9)
        elif self.facing == 'left':
            self.set_state("idle_left", finish_animation=True, last_frame=9)

    def shoot(self):
        self.attacking = True
        self.cooling_down = True
        self.shot_ready = True

    def stop_shot(self, before_shot = False):
        self.attacking = False
        self.cooling_down = False
        self.shot_ready = True
        self.cooldown_timer = 0.0
        self.lock_keys()
        if before_shot:
            self.frame = 9
        if self.facing == "right":
            self.set_state("idle_right", finish_animation=True, last_frame=11)
        elif self.facing == "left":
            self.set_state("idle_left", finish_animation=True, last_frame=11)

    def walking(self) -> bool:
        return self.state == 'walking_left' or self.state == 'walking_right'
    
    def running(self) -> bool:
        return self.state == "running_left" or self.state == "running_right"
    
    def jumping(self) -> bool:
        return self.state == 'jumping_left' or self.state == 'jumping_right'
    
    def move(self):
        self.idle = False
        self.crouching = False
    
    def jump(self):
        # Set the physics and state values #
        self.vel[1] = self.jump_force
        self.airborn = True
        self.grounded = False
        self.gaining = True
        self.jump_hold_time = 0.0

        if self.facing == 'left':
            self.set_state('jumping_left')
        else:
            self.set_state('jumping_right')

    

    def get_weapon(self):
        shot_y = self.position[1] + 9
        if self.crouching:
            shot_y += 8

        if self.facing == 'left':
            shot_position = vec(self.position[0] - 10, shot_y)
        else:
            shot_position = vec(self.position[0] + self.get_width() - 14, shot_y)
        
        self.shot_ready = False

        return Shot(shot_position, self.facing)
    
    def attack(self):
        self.attacking = False



    #   ----- Event Handling -----  #
    def check_left(self):
        #   Left Motion #
        if EM.is_active('motion_left'):
            self.facing = 'left'
            
            #   Mid-air Motion (Left)
            if self.airborn or self.jumping():
                #   Jump Left
                if self.state == 'jumping_right':
                    self.set_state('jumping_left')
                    EM.deactivate('motion_right')
                    if self.vel[0] >= self.max_speed:
                        self.vel[0] *= -1
                    else:
                        self.vel[0] = -self.speed
                
                #   Move Left
                else:
                    self.move()
                    EM.deactivate('motion_right')

                    if abs(self.vel[0]) >= self.max_speed:
                        self.vel[0] *= -1
                    else:
                        self.vel[0] = -self.speed


            #   Grounded Motion (Left)
            elif not self.walking() and not self.running():
                self.move()
                self.set_state('walking_left')
                EM.deactivate('motion_right')

                if abs(self.vel[0]) >= self.max_speed:
                    self.vel[0] *= -1
                else:
                    self.vel[0] = -self.speed

        else:
            #   Idle
            if not self.idle and not self.jumping() and self.facing == 'left':
                self.set_idle('left')

    def check_right(self):
        #   Right Motion    #
        if EM.is_active('motion_right'):
            self.facing = 'right'

            #   Mid-air Motion (Right)
            if self.airborn or self.jumping():
                #   Jump Right
                if self.state == 'jumping_left':
                    self.set_state('jumping_right')
                    EM.deactivate('motion_left')
                    if abs(self.vel[0]) >= self.max_speed:
                        self.vel[0] *= -1
                    else:
                        self.vel[0] = self.speed
                
                #   Move Right
                else:
                    self.move()
                    EM.deactivate('motion_left')
                    if abs(self.vel[0]) >= self.max_speed:
                        self.vel[0] *= -1
                    else:
                        self.vel[0] = self.speed

            #   Grounded Motion (Right)
            elif not self.walking() and not self.running():
                self.move()
                self.set_state('walking_right')
                EM.deactivate('motion_left')
                if abs(self.vel[0]) >= self.max_speed:
                    self.vel[0] *= -1
                else:
                    self.vel[0] = self.speed
        else:
            #   Idle
            if not self.idle and not self.jumping() and self.facing == 'right':
                self.set_idle('right')

    def check_up(self):
        if EM.is_active('motion_up'):
            pass

    def check_down(self):
        #   Start Crouching
        if EM.is_active('motion_down'):
            if not self.crouching:
                self.crouch()

        #   Stop Crouching
        else:
            if self.crouching:
                # if not self.airborn:
                #     self.set_idle(self.facing)
                self.exit_crouch()

    def check_interact(self):
        #   Jumping / Sliding   #
        if EM.is_active('interact'):
            #   Slide attack
            if self.crouching:
                return
            
            if not self.gaining:
                #   Second Jump Press (Mid-air boost)   #
                if self.airborn and not self.grounded:
                    if not self.boosting:
                        #   Boost (1st upgrade)   #
                        if self.state == "jumping_left":
                            self.vel[0] = -self.boost_force
                        else:
                            self.vel[0] = self.boost_force
                        self.boosting = True

                #   First Jump Press (From ground)    #
                elif self.grounded:
                    self.jump()
                    
            #   Do nothing while gaining
            else:
                pass
        else:
            #   Stop gaining after button is released
            if self.airborn:
                self.gaining = False
                self.jump_hold_time = self.jump_hold_max

    def check_attack(self):
        #   Shot Attack (X)
        if EM.is_active('attack1'):
            if abs(self.vel[0]) != 0:
                return
            if self.state != "shooting_right" and self.state != "shooting_left":
                if self.facing == "right":
                    self.set_state("shooting_right")
                elif self.facing == "left":
                    self.set_state("shooting_left")
            elif self.frame == 6:
                if not self.cooling_down:
                    self.shoot()
            else:
                return

        #   Stop Shooting
        elif self.attacking:
            self.stop_shot()

        elif self.state == "shooting_right" or self.state == "shooting_left":
            self.stop_shot(before_shot=True)

    def handle_events(self):
        if not self.visible:
            return
        
        if self.key_lock:
            return
        
        if not self.crouching and not self.attacking:
            self.check_left()
            self.check_right()
            self.check_up()
        
        if not self.attacking:
            self.check_down()
            self.check_interact()

        if not self.crouching and not self.switching_states:
            self.check_attack()
    

    #   ----- Updating  -----   #
    def accel(self, seconds):
        """Accelerate to max speed and stay at that speed"""
        #   Moving Right    #
        if self.vel[0] > 0:
            self.vel[0] += self.acceleration * seconds
            if self.vel[0] > self.max_speed:
                self.vel[0] = self.max_speed
            elif not self.running() and self.vel[0] >= self.running_speed:
                self.set_state("running_right", optional_start_frame=self.frame)
        elif self.vel[0] < 0:
            self.vel[0] -= self.acceleration * seconds
            if self.vel[0] < -self.max_speed:
                self.vel[0] = -self.max_speed
            elif not self.running() and self.vel[0] <= -self.running_speed:
                self.set_state("running_left", optional_start_frame=self.frame)

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

    def land(self):
        """Called when the player is airborne and collides with something below it"""
        #   Reset states
        self.airborn = False
        self.grounded = True
        self.gaining = False
        self.boosting = False

        #   Set the y velocity to 0
        self.vel[1] = 0

        #  Reset animation based on horizontal velocity and facing
        if self.vel[0] < 0:
            self.set_state('walking_left')
        elif self.vel[0] > 0:
            self.set_state('walking_right')
        else:
            if self.facing == 'left':
                self.set_state('idle_left')
            else:
                self.set_state('idle_right')

        #   Deactivate the interact button
        EM.deactivate('interact')
            

    def damage(self, enemy):
        """Apply damage from an enemy and start invulnerability cooldown."""
        if not self.vulnerable or not self.visible:
            return

        damage_amount = enemy.get_damage()
        self.hp -= damage_amount
        if self.hp < 0:
            self.hp = 0

        self.vulnerable = False
        self.damage_timer = 0.0

        if self.crouching:
            self.crouching = False
            EM.deactivate("motion_down")

        print("HP: ", self.hp)

        # Knockback
        if hasattr(enemy, 'position'):
            if enemy.position[0] < self.position[0]:
                self.vel[0] = self.speed
            else:
                self.vel[0] = -self.speed

        self.airborn = True
        self.grounded = False

    def update_vertical(self, seconds):
        """Update the player's vertical (y axis) velocity"""
        #   Apply gravity when airborne
        if self.airborn or not self.grounded:
            if self.gaining and self.jump_hold_time < self.jump_hold_max and self.vel[1] < 0:
                self.vel[1] -= self.jump_hold_gravity * seconds
                self.jump_hold_time += seconds
                if self.jump_hold_time >= self.jump_hold_max:
                    self.gaining = False
                    EM.deactivate("interact")
            # elif EM.is_active('interact') and self.vel[1] >= 0:
            #     self.vel[1] = 0
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

    def get_camera_position(self):
        return self.camera.get_position()
    
    # def set_camera_position(self, direction=0, lock = False):
    #     """
    #     Set the camera's position to the desired position.
    #     Directions:
    #     0 -> right; 1 -> left; 2 -> idle
    #     """

    #     #   Facing Right
    #     if direction == 0:
    #         if lock:
    #             self.cam_pos[0] = int(self.position[0])
    #         else:
    #             self.cam_pos[0] = int(self.position[0] + self.cam_delta)
    #         self.idle_counter = 0

    #     #   Facing Left
    #     elif direction == 1:
    #         if lock:
    #             self.cam_pos[0] = int(self.position[0])
    #         else:
    #             self.cam_pos[0] = int(self.position[0] - self.cam_delta)
    #         self.idle_counter = 0

    #     #   Idle
    #     else:
    #         if self.facing == "right":
    #             self.cam_pos[0] = int(self.position[0])
    #         elif self.facing == "left":
    #             self.cam_pos[0] = int(self.position[0])

    
    # def camera_in_position(self):
    #     """Check if the camera is in the desired position"""
    #     #   Facing Right
    #     if self.vel[0] > 0:
    #         return int(self.cam_pos[0]) == int(self.position[0] + self.cam_delta)
        
    #     #   Facing Left
    #     elif self.vel[0] < 0:
    #         return int(self.cam_pos[0]) == int(self.position[0] - self.cam_delta)
        
    #     #   Idle
    #     else:
    #         return int(self.cam_pos[0]) == int(self.position[0])


    def update_cooldown(self, seconds):
        if self.cooling_down:
            self.cooldown_timer += seconds
            if self.cooldown_timer >= self.shot_cooldown:
                self.cooling_down = False
                self.shot_ready = True
                self.cooldown_timer = 0.0


    def update_animation(self, seconds):
        if self.switching_states:
            if self.animation_timer >= (1/self.get_fps()):
                if self.frame == self.last_frame:
                    self.state = self.next_state
                    self.frame = self.get_current_state().get_starting_frame()
                    self.animation_timer = 0.0
                    self.switching_states = False
                    self.unlock_keys()
                    self.set_image()
                    return
                else:
                    self.frame += 1
                    self.animation_timer = 0.0
                    self.set_image()
                    return
            else:
                self.animation_timer += seconds
                
        else:
            Animated.update(self, seconds)

    def update_vulnerability(self, seconds):
        if not self.vulnerable:
            self.damage_timer += seconds
            if self.damage_timer >= self.damage_cooldown:
                self.vulnerable = True
                self.damage_timer = 0.0


    def update(self, seconds):
        if not self.visible:
            return
        
        # print("State:", self.state)
        # print("X Vel:", self.vel[0])

        #   Update Animation    #
        self.update_animation(seconds)

        #   Update I-frames #
        self.update_vulnerability(seconds)

        #   Update Attack Cooldowns #
        self.update_cooldown(seconds)

        if not self.switching_states:
            #   Update Physics  #
            self.update_movement(seconds)

            #   Update Camera Position  #
            self.camera.update(seconds, self.position.copy(), self.vel.copy(),
                            self.get_size(), self.facing, self.max_speed)

        
        