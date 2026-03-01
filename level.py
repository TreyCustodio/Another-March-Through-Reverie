import pygame
import numpy as np
import time
import sys
import os

from globals import *
from UI import *
from utils import editor


#   Initialize the modules  #
pygame.init()
pygame.joystick.init()

pygame.display.set_caption("AMTR Level Editor")
icon = pygame.image.load(os.path.join("images", "icon.png"))
pygame.display.set_icon(icon)


#   Initialize the Engines  #
# event_manager = EventManager.getInstance()
# audio_manager = AudioManager.getInstance()
# display_manager = DisplayManager.getInstance()


#   Initialize the Display  #
flags = pygame.SCALED# | pygame.FULLSCREEN #| pygame.NOFRAME
screen = pygame.display.set_mode(list(map(int, UPSCALED)), flags=flags)
drawSurface = pygame.Surface(list(map(int, SCREEN_SIZE)))
# pygame.mouse.set_visible(False)



#   Vars for FPS Analysis  #
start_time = time.time()
fps = 0.0
frame_count = 0
gameClock = pygame.time.Clock()

editor.load()

#   Main Loop   #
RUNNING = True
while RUNNING:
    #   (1) Draw    #
    pygame.transform.scale(drawSurface,
                            list(map(int, UPSCALED)),
                            screen)
    pygame.display.flip()
    editor.draw(drawSurface)



    #   (2) Handle Events   #
    RUNNING = editor.handle_events()
    if not RUNNING:
        pygame.quit()
        sys.exit()


    #   (3) Update  #
    else:
        #   Tick the clock
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000

        #   Update the modules  #
        editor.update(seconds)