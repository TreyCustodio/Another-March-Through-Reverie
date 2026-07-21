import os
import pygame

from pygame import font, Rect, transform

from globals import vec, GRAVITY, UPSCALED
from UI import EventManager, AudioManager, SpriteManager
from . import Drawable, State, Animated
from .camera import Camera

from .weapons import *


EM = EventManager.getInstance()
AM = AudioManager.getInstance()
SM = SpriteManager.getInstance()

BASE_WIDTH = 48
BASE_HEIGHT = 48
"""
    (1) Fix Collision Rect
    (2) Fix sprite positions on shooting + hovering state
    (3) Implement Aerial Movement
    (4) Fix Physics
        (a) Weird sliding glitch when turning right while still holding left
        (b) Landing while flying; could be a sprite position bug
        (c) Make crouch() smoother -> experiment with deceleration
        (d) Shouldn't be able to hold boost button and keep boosting
    (5) Make Shooting smoother
        (a) Transition to hovering while shooting
        (b) Fix collision detection while shooting in the air
"""


class PlayerLoader:
    """Use this class to ensure that only one player is ever loaded"""
    _INSTANCE = None

    @classmethod
    def get_player(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = Player()

        return cls._INSTANCE
    

# class Camera:
#     """Determines what the player sees"""
#     #   (1) KEEP THE WEAVER CENTERED HORIZONTALLY

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

        walk_fps = 32
        run_fps = 32
        # shot_fps = 64
        # shot_fps = 16
        
        self.states = {
            # state: [file_name, starting_frame, row, fps, nFrames]
            'idle': State("weaver.png", starting_frame=0, row=0, fps=16, num_frames=48),
            'idle_right': State("weaver.png", 0, 0, 16, 48),
            'idle_left': State("weaver.png", 0, 1, 16, 48),

            'walking_right': State(file_name="weaver_walk.png", starting_frame=0, row=0, fps=walk_fps, num_frames=10),
            'walking_left': State("weaver_walk.png", 0, 0, walk_fps, 10, flip_x=True),

            'running_right': State("weaver_run.png", 0, 0, run_fps, 9, flip_x=False),
            'running_left': State("weaver_run.png", 0, 0, run_fps, 9, flip_x=True),

            'crouching_right': State("weaver_crouch.png", 0, 0, 32, 11, loop=True, loop_start = 3, loop_end=5, loop_fps = 32, flip_x=False),
            'crouching_left': State("weaver_crouch.png", 0, 0, 32, 11, loop=True, loop_start = 3, loop_end=5, loop_fps = 32, flip_x=True),

            'shooting_right': State("weaver_shot.png", 0, 0, 64, 12, loop = True, loop_start = 3, loop_end = 8, loop_fps= 64, flip_x=False),
            'shooting_left': State("weaver_shot.png", 0, 0, 64, 12, loop=True, loop_start = 3, loop_end = 8, loop_fps = 64, flip_x=True),

            'hovering_right': State("weaver_jump.png", row = 0, starting_frame = 0, fps = 64, num_frames = 13, loop=True, loop_start = 5, loop_end = 8, loop_fps=12),
            'hovering_left': State("weaver_jump.png", row = 1, starting_frame = 0, fps = 64, num_frames = 13, loop=True, loop_start = 7, loop_end = 8, loop_fps=12),

            'flying_right': State("weaver_jump.png", row = 2, starting_frame = 0, fps = 64, num_frames = 13, loop=True, loop_start = 5, loop_end = 8, loop_fps=12),
            'flying_left': State("weaver_jump.png", row = 3, starting_frame = 0, fps = 64, num_frames = 13, loop=True, loop_start = 7, loop_end = 8, loop_fps=12),

            'aerial_shot_right': State("weaver_shot.png", 0, 0, 64, 12, loop = True, loop_start = 3, loop_end = 8, loop_fps= 64, flip_x=False),
            'aerial_shot_left': State("weaver_shot.png", 0, 0, 64, 12, loop=True, loop_start = 3, loop_end = 8, loop_fps = 64, flip_x=True),


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
        self.max_speed = 400
        self.running_speed = 250
        self.speed_cap = 800
        self.weight = 15
        self.acceleration = 120
        self.deceleration = 120
        self.boost_deceleration = 10

        self.jump_force = -160
        self.jump_acceleration = 300
        self.jump_hold_max = 0.40
        self.jump_hold_time = 0.0
        self.jump_hold_gravity = 180
        self.boost_force = 400

        self.drop_force = 160
        self.drop_acceleration = 300
        self.vel = vec(0,0)

        #   Weapon Variables    #
        self.shot_cooldown = 0.1
        self.boost_cooldown = 0.1
        self.cooldown_timer = 0.0
        self.boost_frame = 0
        self.boost_lifetime = 8

        #   Physics States  #
        self.attacking = False
        self.shot_ready = True
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


    # ===================================


    """
    --------- Getters and Setters ------------
    """
    def lock_keys(self):
        self.key_lock = True

    def unlock_keys(self):
        self.key_lock = False

    def set_visible(self):
        self.visible = True

    def set_invisible(self):
        self.visible = False
    
    def get_camera_position(self):
        """Return the camera's position"""
        return self.camera.get_position()
    
    def lock_camera(self):
        self.camera_lock = True

    def free_camera(self):
        self.camera_lock = False

    def get_collision_rect(self) -> Rect:
        """Return the collision rect"""
        return Rect((self.position[0] + 6, self.position[1]), (BASE_WIDTH - 14, BASE_HEIGHT))

    def get_hit_box(self) -> Rect:
        """Return the player's hit box"""
        return

    def set_position(self, position):
        self.position = position
        self.cam_pos = position.copy()

    def set_image(self):
        Animated.set_image(self, pre_loaded=True, player = True)

    def play_animation(self, state, starting_frame, ending_frame):
        """Play an animation without switching states"""
        Animated.play_animation(self, state, starting_frame, ending_frame)

    def get_current_state(self):
        return self.states[self.state]
    
    def get_num_frames(self):
        return self.get_current_state().get_num_frames()
    
    def get_fps(self):
        return self.get_current_state().get_fps()

    def get_loop_fps(self):
        return self.get_current_state().get_loop_fps()
    
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
            #   Adjust offsets
            ##  Hovering
            if (not self.airborn) and (
                (state == "hovering_left" and self.state != "hovering_right") or (state == "hovering_right" and self.state != "hovering_left")
                ):
                pass
                # self.position[1] -= 9
            
            ## Shooting
            elif state == "shooting_right":
                pass
            elif state == "shooting_left":
                # self.position[0] -= 11
                pass

            #   Set the state
            self.state = state
            if optional_start_frame != -1:
                self.frame = optional_start_frame
            else:
                self.frame = self.get_current_state().get_starting_frame()
        
        

        #   Set the image
        self.set_image()

    def set_idle(self, direction = 'left'):
        if self.airborn:
            if direction == 'left':
                self.set_state('hovering_left')
                self.facing = 'left'
                
            elif direction == 'right':
                self.set_state('hovering_right')
                self.facing = 'right'
        else:
            if direction == 'left':
                self.set_state('idle_left')
                self.facing = 'left'
                
            elif direction == 'right':
                self.set_state('idle_right')
                self.facing = 'right'

        self.idle = True

    def move(self):
        self.idle = False
        self.crouching = False
        if self.facing == "left":
            self.vel[0] = -self.speed
        else:
            self.vel[0] = self.speed
    
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

    def turn(self):
        """Turn around"""
        if abs(self.vel[0]) >= self.max_speed:
            self.vel[0] *= -1
        else:
            self.vel[0] = -self.speed

    def crouch(self):
        if abs(self.vel[0]) <= 400:
            # self.vel[0] = 0
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

    def boost(self):
        if self.facing == "left":
            self.vel[0] += -self.boost_force
            if self.vel[0] < -self.speed_cap:
                self.vel[0] = -self.speed_cap
            if not self.airborn and not self.running():
                self.set_state("running_left", optional_start_frame=self.frame % 9)
        
        elif self.facing == "right":
            self.vel[0] += self.boost_force
            if self.vel[0] > self.speed_cap:
                self.vel[0] = self.speed_cap
            if not self.airborn and not self.running():
                self.set_state("running_right", optional_start_frame=self.frame % 9)
        
        self.boosting = True
        self.cooling_down = True
        
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

        if self.airborn:
            if self.facing == "right":
                self.set_state("hovering_right", finish_animation=True, last_frame=11)
            elif self.facing == "left":
                self.set_state("hovering_left", finish_animation=True, last_frame=11)
        else:
            if self.facing == "right":
                self.set_state("idle_right", finish_animation=True, last_frame=11)
            elif self.facing == "left":
                self.set_state("idle_left", finish_animation=True, last_frame=11)
    
    def land(self):
        """Called when the player is airborne and collides with something below it"""
        if self.shooting():
            return
        
        #   Reset states
        self.airborn = False
        self.vel[1] = 0
        EM.deactivate('interact')


        if self.facing == "left":
            self.set_state("idle_left", finish_animation=True, last_frame=12)
        elif self.facing == "right":
            self.set_state("idle_right", finish_animation=True, last_frame=12)

        return
    
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


    # ===================================


    """
    --------- Drawing Functions -------------
    """
    def draw_shadows(self, drawSurf):
        """Draw the boost effect"""
        if abs(self.vel[0]) >= self.max_speed:
            #   Set the number of frames to draw
            if self.boost_frame >= 0 and self.boost_frame < 2:
                frames = 1

            elif self.boost_frame >= 2 and self.boost_frame < 4:
                frames = 2
            
            elif self.boost_frame >= 4 and self.boost_frame < 5:
                frames = 3

            elif self.boost_frame >= 5 and self.boost_frame < 6:
                frames = 2
            
            elif self.boost_frame >= 6:
                frames = 1

            #   Draw the frames based on the player's direction
            if self.facing == "left":
                for i in range(1, frames + 1):
                    drawSurf.blit(self.image, vec(self.position[0] + (6 * i), self.position[1]) - Drawable.CAMERA_OFFSET)

            elif self.facing == "right":
                for i in range(1, frames + 1):
                    drawSurf.blit(self.image, vec(self.position[0] - (6 * i), self.position[1]) - Drawable.CAMERA_OFFSET)
            
    def draw(self, drawSurf, draw_rect = True):
        """Draw the player"""
        if not self.visible:
            return
        
        if self.boosting:
            #   Draw Max Speed Shadow   #
            self.draw_shadows(drawSurf)
        
        #   Draw a black outline around the player sprite   
        outline_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        mask = pygame.mask.from_surface(self.image)
        mask.to_surface(outline_surface, setcolor=(38, 4, 56, 255), unsetcolor=(0,0,0,0))

        base_pos = list(map(int, self.position - Drawable.CAMERA_OFFSET))
        outline_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for offset in outline_offsets:
            drawSurf.blit(outline_surface, (base_pos[0] + offset[0], base_pos[1] + offset[1]))
        
        #   Display the collision rect  #
        if draw_rect:
            rect = self.get_collision_rect()
            rect = rect.move(-Drawable.CAMERA_OFFSET[0], -Drawable.CAMERA_OFFSET[1])
            pygame.draw.rect(drawSurf, (255, 20, 20), rect, 1)

        #   Display the velocity    #
        velocity = str(round(self.vel[0], 2))
        if abs(self.vel[0]) == self.max_speed:
            img = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16).render("Velocity X: " + str(velocity), False, (255,0,0), (0,0,0))
        else:
            img = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16).render("Velocity X: " + str(velocity), False, (255,255,255), (0,0,0))

        drawSurf.blit(img, vec(self.position[0] + self.get_width() // 2 - img.get_width() // 2, self.position[1] - img.get_height() - 48) - Drawable.CAMERA_OFFSET)


        velocity2 = str(round(self.vel[1], 2))
        if abs(self.vel[1]) == self.max_speed:
            img = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16).render("Velocity Y: " + str(velocity2), False, (255,0,0), (0,0,0))
        else:
            img = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16).render("Velocity Y: " + str(velocity2), False, (255,255,255), (0,0,0))

        drawSurf.blit(img, vec(self.position[0] + self.get_width() // 2 - img.get_width() // 2, self.position[1] - img.get_height() - 8) - Drawable.CAMERA_OFFSET)
        
        
        #   Draw the Player's main sprite   #
        super().draw(drawSurf, False)

        #   Draw the top-layer boost effect #
        # if self.boosting:
        #     img = SM.getSprite(fileName="fire_shield.png", offset=(self.boost_frame, 0), enemy=False)
        #     pos_offset = vec(-4,0)

        #     if self.facing == "left":
        #         img = pygame.transform.flip(img, True, False)
        #         pos_offset[0] = 12

        #     img.set_alpha(100)

        #     drawSurf.blit(img, list(map(int, self.position - pos_offset - Drawable.CAMERA_OFFSET)))

    
    # ===================================


    """
    ------- Boolean Functions  -------
    """
    def stationary(self) -> bool:
        """Return True if the player is standing still"""
        return not self.walking() and not self.running() and not self.flying()
    
    def is_boosting(self) -> bool:
        return self.boosting
    
    def flying(self) -> bool:
        """Return True if the player is moving in the air"""
        return self.state == "flying_left" or self.state == "flying_right"
    
    def walking(self) -> bool:
        """Return True if the player is moving, but not at top speed"""
        return self.state == 'walking_left' or self.state == 'walking_right'

    def running(self) -> bool:
        """Return True if the player is running at top speed"""
        return self.state == "running_left" or self.state == "running_right"
    
    def moving(self) -> bool:
        """Return True if the player is moving at all"""
        return self.walking() or self.running() or self.flying()
    
    def shooting(self) -> bool:
        """Return True if the player is shooting th obliterator"""
        return self.state == "shooting_left" or self.state == "shooting_right" or self.state == "aerial_shot_left" or self.state == "aerial_shot_right"
    
    def aerial(self) -> bool:
        """Not implemented yet"""
        return self.airborn
    

    # ===================================


    """
    ------- Checking for and Handling Input  -------
    * Four Primary States *
    (1) Stationary
    (2) Dashing
        (a) walking
        (b) running at top speed
    (3) Crouching
    (4) Aerial
    """
    def check_left(self):
        """Check for left motion"""
        if EM.is_active('motion_left'):
            self.facing = 'left'
            
            if self.airborn:
                #   Start Flying
                if self.stationary():
                    EM.deactivate("motion_right")
                    self.set_state("flying_left")
                    self.move()

                #   Turn Around
                elif self.moving():
                    if self.state == "flying_right":
                        self.turn()
                        self.set_state("flying_left", optional_start_frame=self.frame % 9)
                return
            
            #   Turn around
            if self.state == "running_right":
                self.set_state("running_left", optional_start_frame=self.frame % 9)
                self.turn()
                EM.deactivate('motion_right')
                return

            elif self.state == "walking_right":
                self.set_state('walking_left')
                self.turn()
                EM.deactivate('motion_right')
                return

            #   Start walking
            if not self.walking() and not self.running():
                #   The player is idle
                self.move()
                self.set_state('walking_left')
                EM.deactivate('motion_right')

        else:
            if self.state == "walking_left" or self.state == "running_left":
                self.set_idle(self.facing)
            
            elif self.state == "flying_left":
                self.set_idle(self.facing)

    def check_right(self):
        """Check for right motion"""
        if EM.is_active('motion_right'):
            self.facing = 'right'
            
            if self.airborn:
                #   Start Flyin'
                if self.stationary():
                    EM.deactivate("motion_left")
                    self.set_state("flying_right")
                    self.move()

                #   Turn Around
                elif self.moving():
                    if self.state == "flying_left":
                        self.turn()
                        self.set_state("flying_right", optional_start_frame=self.frame % 9)
                return
            
            #   Turn around
            if self.state == "running_left":
                self.set_state("running_right", optional_start_frame=self.frame % 9)
                self.turn()
                EM.deactivate('motion_left')
                return

            elif self.state == "walking_left":
                self.set_state('walking_right')
                self.turn()
                EM.deactivate('motion_left')
                return
            
            #   Start walking
            if not self.walking() and not self.running():
                #   The player is idle
                self.move()
                self.set_state('walking_right')
                EM.deactivate('motion_left')

        else:
            if self.state == "walking_right" or self.state == "running_right":
                self.set_idle(self.facing)

            elif self.state == "flying_right":
                self.set_idle(self.facing)


    def check_up(self):
        """Check for upward motion"""
        #   Upward Movement   #
        if EM.is_active('motion_up'):
            #   Enter the air
            if not self.airborn:
                self.vel[1] = self.jump_force

                if self.stationary():
                    if self.facing == "left":
                        self.set_state("hovering_left")
                    elif self.facing == "right":
                        self.set_state("hovering_right")
                
                elif self.moving():
                    if self.facing == "left":
                        self.set_state("flying_left")

                    elif self.facing == "right":
                        self.set_state("flying_right")

                self.airborn = True
            else:
                if self.vel[1] > self.jump_force:
                    self.vel[1] = self.jump_force
            
        else:
            if self.airborn and not EM.is_active("motion_down"):
                self.vel[1] = 0

    def check_down(self):
        """Check for downward motion"""
        #   Start Crouching
        if EM.is_active('motion_down'):
            if self.airborn: 
                if self.vel[1] < self.drop_force:
                    self.vel[1] = self.drop_force

            elif not self.crouching:
                self.crouch()

        #   Stop Crouching
        else:
            if self.airborn and not EM.is_active("motion_up"):
                self.vel[1] = 0
                
            elif self.crouching:
                # if not self.airborn:
                #     self.set_idle(self.facing)
                self.exit_crouch()

    def check_interact(self):
        """Check for *Interact* """
        return
        #   Jumping / Sliding   #
        if EM.is_active('interact'):
            if not self.airborn:
                if self.stationary():
                    if self.facing == "left":
                        self.set_state("hovering_left")
                    elif self.facing == "right":
                        self.set_state("hovering_right")
                
                elif self.moving():
                    if self.facing == "left":
                        self.set_state("flying_left")

                        # self.set_state("hovering_left")
                        # self.set_state("flying_left", finish_animation=True, last_frame=5)


                    elif self.facing == "right":
                        self.set_state("flying_right")

                        # self.set_state("hovering_right")
                        # self.set_state("flying_right", finish_animation=True, last_frame=5)


                self.airborn = True
            
            #   Enter the air
            self.vel[1] = self.jump_force

            #   Slide attack
            if self.crouching:
                return
        else:
            if not EM.is_active('motion_down'):
                self.vel[1] = 0
            
    def check_attack(self):
        """Check for *Attack 1* """
        if EM.is_active('attack1'):

            #   Stationary -> Obliterator   #
            if self.stationary():
                #   Aerial Shot
                if self.airborn:
                    if self.state != "aerial_shot_right" and self.state != "aerial_shot_left":
                        if self.facing == "right":
                            self.set_state("aerial_shot_right")
                        elif self.facing == "left":
                            self.set_state("aerial_shot_left")
                    elif self.frame == 6:
                        if not self.cooling_down:
                            self.shoot()
                    else:
                        return
                
                #   Ground Shot
                elif abs(self.vel[0]) <= 320:
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
            
            #   Dashing -> Way Boost
            elif self.moving():
                # EM.deactivate('attack1')
                if not self.boosting and self.shot_ready:
                    self.boost()
                

        #   Stop Shooting
        elif self.attacking:
            self.stop_shot()

        elif self.state == "shooting_right" or self.state == "shooting_left" or self.state == "aerial_shot_left" or self.state == "aerial_shot_right":
            self.stop_shot(before_shot=True)

    def check_special(self):
        """Check *Special* """
        return
    
    def check_evasive(self):
        """Check *Evasive* """
        return
    
    def check_pause(self):
        """Check *Pause* """
        return

    def check_map(self):
        """Check *Map* """
        return
    

    def handle_events(self):
        if not self.visible:
            return
        
        if self.key_lock:
            return
        
        if self.switching_states:
            return
        
        if not self.crouching and not self.attacking:
            self.check_left()
            self.check_right()
        
        if not self.attacking:
            self.check_down()
            self.check_up()
            self.check_interact()


        if not self.crouching:
            self.check_attack()
    

    # ===================================


    """
    ------ Update Player Data ------
    """
    def accel(self, seconds):
        """Accelerate to max speed and stay at that speed"""
        #   Move Right  #
        if self.state == "walking_right" or self.state == "flying_right":
            self.vel[0] += self.acceleration * seconds
            #   Reach top speed
            if self.vel[0] >= self.running_speed:
                self.vel[0] = self.max_speed
                if self.flying():
                    pass
                elif not self.running():
                    self.set_state("running_right", optional_start_frame=self.frame % 9)
        
        #   Move Left   #
        elif self.state == "walking_left" or self.state == "flying_left":
            self.vel[0] -= self.acceleration * seconds
            #   Reach top speed
            if self.vel[0] <= -self.running_speed:
                self.vel[0] = -self.max_speed
                if self.flying():
                    pass
                elif not self.running():
                    self.set_state("running_left", optional_start_frame=self.frame % 9)

    def decel(self, seconds):
        """Decelerate to max speed and stay at that speed"""
        #   Moving Right    #
        if self.vel[0] > 0:
            self.vel[0] -= (self.deceleration * self.boost_deceleration) * seconds
            if self.vel[0] <= self.max_speed:
                self.vel[0] = self.max_speed
       
       #    Moving Left #
        else:
            self.vel[0] += (self.deceleration * self.boost_deceleration) * seconds
            if self.vel[0] >= -self.max_speed:
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
        if self.airborn:
            if EM.is_active('motion_down') and not EM.is_active("motion_up"):
                self.vel[1] += self.drop_acceleration * seconds
            elif EM.is_active('motion_up') and not EM.is_active('motion_down'):
                self.vel[1] -= self.jump_acceleration * seconds

        return
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

    def update_cooldown(self, seconds):
        """Update all attack cooldowns and animations"""
        #   Update *Obliterator*
        if self.cooling_down:
            self.cooldown_timer += seconds
            if self.cooldown_timer >= self.shot_cooldown:
                self.cooling_down = False
                self.shot_ready = True
                self.cooldown_timer = 0.0

        #   Update *Way Boost*
        if self.boosting:
            self.boost_frame += 1
            if self.boost_frame == self.boost_lifetime:
                self.boost_frame = 0
                self.boosting = False

    def update_animation(self, seconds):
        if self.switching_states:
            if self.animation_timer >= (1/self.get_fps()):
                if self.frame == self.last_frame:
                    #   Adjust offset
                    
                    if self.next_state == "idle_left" or self.next_state == "idle_right":
                        ##  Landing
                        if self.state == "hovering_left" or self.state == "hovering_right":
                            self.position[1] += 9
                    
                        ##  Stopping shot
                        elif self.next_state == "idle_left" and self.state == "shooting_left":
                            self.position[0] += 11

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

        # print(self.position)
        # print("===============\n")