from . import vec

#   16:9 Aspect Ratio   #
SCREEN_SIZE = vec(640,360)
SCREEN_SIZE = vec(500,240)

               
#   Universal Upscale Value -- all images will be scaled to this value  #
SCALE_FACTOR = 1

#   Upscaled Screen Size    #
UPSCALED = SCREEN_SIZE * SCALE_FACTOR

#   Gravity #
GRAVITY = 500
