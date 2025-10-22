import pygame
import numpy as np
import time
import sys
import os

from globals import *
from UI import *


#   Initialize the modules  #
pygame.init()
pygame.joystick.init()

pygame.display.set_caption("Another March Through Reverie (AMTR)")
icon = pygame.image.load(os.path.join("images", "icon.png"))
pygame.display.set_icon(icon)


#   Initialize the Engines  #
event_manager = EventManager.getInstance()
audio_manager = AudioManager.getInstance()
display_manager = DisplayManager.getInstance()


#   Initialize the Display  #
flags = pygame.SCALED #| pygame.FULLSCREEN#| pygame.NOFRAME | pygame.FULLSCREEN
screen = pygame.display.set_mode(list(map(int, UPSCALED)), flags=flags)
drawSurface = pygame.Surface(list(map(int, SCREEN_SIZE)))
# pygame.mouse.set_visible(False)



#   Vars for FPS Analysis  #
start_time = time.time()
fps = 0.0
frame_count = 0
gameClock = pygame.time.Clock()




#   Main Loop   #
RUNNING = True
while RUNNING:
    #   (1) Draw    #
    pygame.transform.scale(drawSurface,
                            list(map(int, UPSCALED)),
                            screen)
    pygame.display.flip()
    display_manager.draw(drawSurface)



    #   (2) Handle Events   #
    RUNNING = event_manager.main()
    if not RUNNING:
        pygame.quit()
        sys.exit()


    #   (3) Update  #
    else:
        #   Tick the clock
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000

        #   Update the modules  #
        event_manager.update_buffer(seconds)

        display_manager.handle_events()
        
        display_manager.update(seconds)

        audio_manager.update(seconds)
    

        #   Debugging Options   #
        #   Calculate and Display FPS
        frame_count += 1
        if time.time() - start_time > 1:
            #  Should be as close to 60 as possible per the tick(60)
            fps = frame_count / (time.time() - start_time)
            # print("-" * 10)
            # print(f"FPS: {fps:.2f}")
            # print("-" * 10, end="\n\n")
            frame_count = 0
            start_time = time.time()

        display_manager.draw_fps(drawSurface, fps)

        #   Turn music low/off
        AM.bgm_channel.set_volume(0.01)