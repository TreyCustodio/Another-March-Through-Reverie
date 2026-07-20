from . import *

"""
This file contains all the functions necessary
for constructing each room in the game.

The Level Editor will write functions to this file.
"""
def mid_1(obj):
    obj.background = [
        Drawable(vec(0,0), os.path.join("middleground.png"))
    ]
    
    obj.tileset = "mid.png"
    obj.tiles = []


    obj.doors += [
        Door(vec(obj.size[0],0), obj.tileset, (0,0), size = vec(16, obj.size[1]), property = 3),
    ]
    
    for x in range(0, int(obj.size[0]), 16):
        #   Black Tiles (0,0)   #
        for y in range(int(obj.size[1]), int(obj.size[1] - 64), -16):
            obj.tiles += [
                    Tile(vec(x, y), obj.tileset, (0,0))
                ]
        
        #   Red ground (2,1) + (2,0)    #
        obj.tiles += [
            Tile(vec(x, obj.size[1]- 80), obj.tileset, (2,0), property=0),
            Tile(vec(x, obj.size[1] - 64), obj.tileset, (2,1), property=1)
            ]
    
    for y in range(0, int(obj.size[1])):
        obj.tiles += [
            Tile(vec(-16, y), obj.tileset, (0,1), property=1)
        ]

def mid_s1(rm):
    rm.background = [
        Drawable(vec(0,0), os.path.join("yellow.png"))
    ]

    # bk = Drawable(vec(0,0), os.path.join("middleground.png"))
    # bk.image = transform.scale(bk.image, SCREEN_SIZE)
    
    rm.tileset = "mid.png"
    rm.tiles = []
    rm.doors = []

    #   Transition Zone #
    # for y in range(0, int(rm.size[1]), 16):
    rm.doors += [
        Door(vec(-16,0), rm.tileset, (0,0), size = vec(16, rm.size[1]), property = 3),
    ]

    #   Ceiling #
    for x in range(0, int(rm.size[0]), 16):
        rm.tiles += [
            Tile(vec(x, -16), rm.tileset, (0,1), property=1)
        ]


    #   Map Tiles   #
    #   Left Edge
    rm.tiles += [
        Tile(vec(0, rm.size[1] - 64), rm.tileset, (0,14), property=0),
        Tile(vec(0, rm.size[1] - 48), rm.tileset, (0,15), property=1),
        Tile(vec(0, rm.size[1] - 32), rm.tileset, (0,0), property=0),
        Tile(vec(0, rm.size[1] - 16), rm.tileset, (0,0), property=0),

        Tile(vec(16, rm.size[1] - 64), rm.tileset, (0,14), property=0),
        Tile(vec(16, rm.size[1] - 48), rm.tileset, (0,15), property=1),
        Tile(vec(16, rm.size[1] - 32), rm.tileset, (0,0), property=0),
        Tile(vec(16, rm.size[1] - 16), rm.tileset, (0,0), property=0),
    ]


    #   Mound 1
    for x in range(16):
        rm.tiles += [
            Tile(vec(32 + (16*x), rm.size[1] - 80), rm.tileset, (x,13), property=0),
            Tile(vec(32 + (16*x), rm.size[1] - 64), rm.tileset, (x,14), property=1),
            Tile(vec(32 + (16*x), rm.size[1] - 48), rm.tileset, (x,15), property=1),

            Tile(vec(32 + (16*x), rm.size[1] - 32), rm.tileset, (0,0), property=1),
            Tile(vec(32 + (16*x), rm.size[1] - 16), rm.tileset, (0,0), property=1),
            Tile(vec(32 + (16*x), rm.size[1]), rm.tileset, (0,0), property=1),
            ]
    
    #   Tiles in between mounds
    for i in range(3):
        rm.tiles += [
            Tile(vec(288 + 16 * i, rm.size[1] - 64), rm.tileset, (0,14), property=0),
            Tile(vec(288 + 16 * i, rm.size[1] - 48), rm.tileset, (0,15), property=1),
            Tile(vec(288 + 16 * i, rm.size[1] - 32), rm.tileset, (0,0), property=0),
            Tile(vec(288 + 16 * i, rm.size[1] - 16), rm.tileset, (0,0), property=0),
        ]
    

    #   Mound 2
    for x in range(16):
        rm.tiles += [
            Tile(vec(336 + (16*x), rm.size[1] - 80), rm.tileset, (x,13), property=0),
            Tile(vec(336 + (16*x), rm.size[1] - 64), rm.tileset, (x,14), property=1),
            Tile(vec(336 + (16*x), rm.size[1] - 48), rm.tileset, (x,15), property=1),

            Tile(vec(336 + (16*x), rm.size[1] - 32), rm.tileset, (0,0), property=1),
            Tile(vec(336 + (16*x), rm.size[1] - 16), rm.tileset, (0,0), property=1),
            Tile(vec(336 + (16*x), rm.size[1]), rm.tileset, (0,0), property=1),
            ]
    
    #   Right Edge
    rm.tiles += [
        Tile(vec(rm.size[0] - 16, rm.size[1] - 64), rm.tileset, (0,14), property=0),
        Tile(vec(rm.size[0] - 16, rm.size[1] - 48), rm.tileset, (0,15), property=1),
        Tile(vec(rm.size[0] - 16, rm.size[1] - 32), rm.tileset, (0,0), property=0),
        Tile(vec(rm.size[0] - 16, rm.size[1] - 16), rm.tileset, (0,0), property=0),

        Tile(vec(rm.size[0] - 32, rm.size[1] - 64), rm.tileset, (0,14), property=0),
        Tile(vec(rm.size[0] - 32, rm.size[1] - 48), rm.tileset, (0,15), property=1),
        Tile(vec(rm.size[0] - 32, rm.size[1] - 32), rm.tileset, (0,0), property=0),
        Tile(vec(rm.size[0] - 32, rm.size[1] - 16), rm.tileset, (0,0), property=0),

        Tile(vec(rm.size[0] - 48, rm.size[1] - 64), rm.tileset, (0,14), property=0),
        Tile(vec(rm.size[0] - 48, rm.size[1] - 48), rm.tileset, (0,15), property=1),
        Tile(vec(rm.size[0] - 48, rm.size[1] - 32), rm.tileset, (0,0), property=0),
        Tile(vec(rm.size[0] - 48, rm.size[1] - 16), rm.tileset, (0,0), property=0),
    ]

    return